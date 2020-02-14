package api

import (
	"bytes"
	"context"
	"fmt"
	"github.com/docker/distribution/uuid"
	"github.com/docker/docker/api/types"
	"github.com/docker/docker/api/types/container"
	"github.com/docker/docker/client"
	"github.com/sirupsen/logrus"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"ppc/metrics"
	"strconv"
	"strings"
	"time"
)

func CheckHandler(w http.ResponseWriter, r *http.Request) {
	metrics.Requests.Inc()

	if r.Method != http.MethodPost {
		http.Error(w, "POST method allowed only!", 400)
		metrics.Errors.Inc()
		return
	}

	err := r.ParseMultipartForm(32 << 20)
	if err != nil {
		logrus.WithError(err).Errorf("Error while parse form")
		Error(w, "Can't parse form")
		metrics.Errors.Inc()
		return
	}

	file, _, err := r.FormFile("uploadfile")
	if err != nil {
		logrus.WithError(err).Errorf("Can't get file via uploadfile")
		Error(w, "Can't get uploaded file")
		metrics.Errors.Inc()
		return
	}

	filename := "/tmp/" + uuid.Generate().String()

	f, err := os.OpenFile(filename, os.O_WRONLY|os.O_CREATE, 0777)
	if err != nil {
		logrus.WithError(err).Errorf("Can't open file")
		Error(w, "Can't write your file")
		metrics.Errors.Inc()
		return
	}

	var buffer = make([]byte, 2)
	_, err = file.Read(buffer)
	file.Seek(0, 0)

	_, err = io.Copy(f, file)
	if err != nil {
		logrus.WithError(err).Errorf("Can't copy file")
		Error(w, "Can't write your file")
		metrics.Errors.Inc()
		return
	}

	file.Close()
	f.Close()

	defer DeleteFile(filename)

	if bytes.Equal(buffer, []byte{'#', '!'}) {
		cmd := exec.Command("dos2unix", filename)
		err = cmd.Run()
		if err != nil {
			logrus.WithError(err).Errorf("Can't convert CRLF")
			Error(w, "Can't convert CRLF")
			metrics.Errors.Inc()
			return
		}
	}

	cli, err := client.NewEnvClient()
	if err != nil {
		logrus.WithError(err).Errorf("Can't get docker cli")
		Error(w, "Can't connect to docker")
		metrics.Errors.Inc()
		return
	}

	defer cli.Close()

	ctx, cancel := context.WithTimeout(context.Background(), 110 * time.Second)
	defer cancel()

	ex, _ := os.Executable()
	cwd := filepath.Dir(ex)

	resp, err := cli.ContainerCreate(ctx, &container.Config{
		Image: "sollos/python3.8-transliterate",
		NetworkDisabled: true,
		Cmd: []string{"/check/check.py"},
	}, &container.HostConfig{
		AutoRemove: false,
		ReadonlyRootfs: true,
		Resources: container.Resources{
			Memory: 50 * 1024 * 1024,
			PidsLimit: 10,
		},
		Binds: []string{
			fmt.Sprintf("%v:/bin/run", filename),
			fmt.Sprintf("%v/check.py:/check/check.py", cwd),
			fmt.Sprintf("%v/images:/images:ro", cwd),
		},
	}, nil, uuid.Generate().String())

	if err != nil {
		logrus.WithError(err).Errorf("Can't create docker container")
		Error(w, "Can't create docker container")
		metrics.Errors.Inc()
		return
	}

	if err := cli.ContainerStart(ctx, resp.ID, types.ContainerStartOptions{}); err != nil {
		logrus.WithError(err).Errorf("Can't start docker container")
		Error(w, "Can't start docker container")
		metrics.Errors.Inc()
		return
	}

	if _, err := cli.ContainerWait(ctx, resp.ID); err != nil {
		if err.Error() == "context deadline exceeded" {
			logrus.WithError(err).Warnf("Global timeout deadline exceeded")
			Answer(w, 0, "", "TIMEOUT")
			metrics.Errors.Inc()
			return
		}

		logrus.WithError(err).Errorf("Can't wait for docker container")
		Error(w, "Some error while running tests")
		metrics.Errors.Inc()
		return
	}

	cmd := exec.Command("docker", "logs", resp.ID)
	buf := new(bytes.Buffer)
	cmd.Stdout = buf
	err = cmd.Run()
	if err != nil {
		logrus.WithError(err).Errorf("Can't execute docker for reading logs")
		Error(w, "Can't read logs")
		metrics.Errors.Inc()
		return
	}

	answer := buf.String()
	answer = strings.TrimSpace(answer)

	if strings.HasPrefix(answer, "INVALID ") {
		testsStr := strings.TrimPrefix(answer, "INVALID ")
		tests, err := strconv.ParseInt(testsStr, 10, 64)
		if err != nil {
			logrus.WithError(err).Errorf("Can't parse output from container")
			Error(w, "Can't parse output from container")
			metrics.Errors.Inc()
			return
		}

		Answer(w, tests, "", "INVALID")
	} else if strings.HasPrefix(answer, "TIMEOUT ") {
		testsStr := strings.TrimPrefix(answer, "TIMEOUT ")
		tests, err := strconv.ParseInt(testsStr, 10, 64)
		if err != nil {
			logrus.WithError(err).Errorf("Can't parse output from container")
			Error(w, "Can't parse output from container")
			metrics.Errors.Inc()
			return
		}

		Answer(w, tests, "", "TIMEOUT")
	} else if strings.HasPrefix(answer, "NO ") {
		stuffStr := strings.TrimPrefix(answer, "NO ")
		stuff := strings.SplitN(stuffStr, " ", 2)

		tests, err := strconv.ParseInt(stuff[0], 10, 64)
		if err != nil {
			logrus.WithError(err).Errorf("Can't parse output from container")
			Error(w, "Can't parse output from container")
			metrics.Errors.Inc()
			return
		}

		Answer(w, tests, stuff[1], "NO")
	} else if answer == "YES" {
		Answer(w, 50, "", "YES")
	} else {
		Error(w, "Unexpected internal error")
	}

	//err = cli.ContainerRemove(context.Background(), resp.ID, types.ContainerRemoveOptions{
	//	RemoveVolumes: true,
	//	RemoveLinks:   false,
	//	Force:         true,
	//})
	//if err != nil {
	//	logrus.WithError(err).Errorf("Can't delete docker container")
	//	return
	//}

	err = cli.Close()
	if err != nil {
		logrus.WithError(err).Infof("Can't close client")
		Error(w, "Can't close docker client")
		return
	}
}
