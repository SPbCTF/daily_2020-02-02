package api

import (
	"github.com/sirupsen/logrus"
	"html/template"
	"net/http"
)

func Error(w http.ResponseWriter, msg string) {
	tmpl, err := template.New("error.html").ParseFiles("frontend/error.html")

	if err != nil {
		logrus.WithError(err).Errorf("Can't parse error.html")
		return
	}

	err = tmpl.Execute(w, msg)
	if err != nil {
		logrus.WithError(err).Errorf("Can't execute error.html")
		return
	}
}
