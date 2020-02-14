package main

import (
	"context"
	"github.com/docker/docker/api/types"
	"github.com/docker/docker/client"
	"github.com/sirupsen/logrus"
	"github.com/spf13/viper"
	"net/http"
	"ppc/api"
	"ppc/logger"
	"ppc/metrics"
)

func main() {
	viper.AutomaticEnv()
	logger.Init()

	mux := api.GetAPI()

	cli, err := client.NewEnvClient()
	if err != nil {
		logrus.WithError(err).Fatalf("Can't get docker cli")
	}

	_, err = cli.ImagePull(context.Background(), "docker.io/sollos/python3.8-transliterate", types.ImagePullOptions{})
	if err != nil {
		logrus.WithError(err).Fatalf("Can't pull image")
	}

	go metrics.ServeMetrics()

	logrus.Fatal(http.ListenAndServe(viper.GetString("LISTEN"), mux))
}
