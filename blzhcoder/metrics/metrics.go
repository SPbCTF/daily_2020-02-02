package metrics

import (
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"github.com/sirupsen/logrus"
	"github.com/spf13/viper"
	"net/http"
)

var (
	Requests = prometheus.NewCounter(prometheus.CounterOpts{
		Name: "requests",
	})

	Errors = prometheus.NewCounter(prometheus.CounterOpts{
		Name: "errors",
	})

	Timeouts = prometheus.NewCounter(
		prometheus.CounterOpts{
			Name: "timeout",
		},
	)

	Invalids = prometheus.NewCounter(
		prometheus.CounterOpts{
			Name: "invalid",
		},
	)

	Success = prometheus.NewCounter(
		prometheus.CounterOpts{
			Name: "success",
		},
	)

	NoAnswers = prometheus.NewCounterVec(prometheus.CounterOpts{
		Name: "no_answers",
	}, []string{
		"level",
		"answer",
	})
)

func init() {
	prometheus.MustRegister(Requests)
	prometheus.MustRegister(Errors)

	prometheus.MustRegister(Timeouts)
	prometheus.MustRegister(Invalids)
	prometheus.MustRegister(Success)
	prometheus.MustRegister(NoAnswers)
}

func ServeMetrics() {
	srv := http.Server{
		Addr:    viper.GetString("OPS_LISTEN"),
		Handler: promhttp.Handler(),
	}

	logrus.Fatal(srv.ListenAndServe())
}
