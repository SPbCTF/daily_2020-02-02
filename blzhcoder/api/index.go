package api

import (
	"github.com/sirupsen/logrus"
	"html/template"
	"net/http"
)

func IndexHandler(w http.ResponseWriter, r *http.Request) {
	tmpl, err := template.New("index.html").ParseFiles("frontend/index.html")

	if err != nil {
		logrus.WithError(err).Errorf("Can't parse index.html")
		Error(w, "Error in parsing template")
		return
	}

	err = tmpl.Execute(w, nil)
	if err != nil {
		logrus.WithError(err).Errorf("Can't execute index.html")
		Error(w, "Error in parsing template")
		return
	}
}
