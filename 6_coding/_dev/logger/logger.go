package logger

import (
	"github.com/sirupsen/logrus"
	"os"
)

func Init() {
	logrus.SetFormatter(&logrus.JSONFormatter{
		DisableTimestamp: false,
		//FullTimestamp:    true,
		//ForceColors:      true,
	})
	logrus.SetReportCaller(true)
	logrus.SetOutput(os.Stdout)
}