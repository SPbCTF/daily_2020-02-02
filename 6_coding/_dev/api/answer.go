package api

import (
	"fmt"
	"github.com/sirupsen/logrus"
	"github.com/spf13/viper"
	"html/template"
	"net/http"
	"ppc/metrics"
)

type Result struct {
	Tests template.HTML
	Answer template.HTML
}

func Answer(w http.ResponseWriter, tests int64, answer string, decision string) {
	tmpl, err := template.New("answer.html").ParseFiles("frontend/answer.html")

	if err != nil {
		logrus.WithError(err).Errorf("Can't parse answer.html")
		return
	}

	if decision == "TIMEOUT" {
		metrics.Timeouts.Inc()

		err = tmpl.Execute(w, &Result{
			Tests:  template.HTML(fmt.Sprintf("%v", tests)),
			Answer: "<b class=\"h4 text-danger\">Превышен таймаут</b>",
		})
		if err != nil {
			logrus.WithError(err).Errorf("Can't execute answer.html")
			return
		}
		return
	}

	if decision == "INVALID" {
		metrics.Invalids.Inc()

		err = tmpl.Execute(w, &Result{
			Tests:  template.HTML(fmt.Sprintf("%v", tests)),
			Answer: "<b class=\"h4 text-danger\">Программа крашнулась :( Иди чини!</b>",
		})
		if err != nil {
			logrus.WithError(err).Errorf("Can't execute answer.html")
			return
		}
		return
	}

	if decision == "NO" {
		if len(answer) < 100 {
			metrics.NoAnswers.WithLabelValues(fmt.Sprintf("%v", tests), answer).Inc()
		}

		err = tmpl.Execute(w, &Result{
			Tests:  template.HTML(fmt.Sprintf("%v", tests)),
			Answer: template.HTML(fmt.Sprintf(
				"Получен ответ на %v-й тест: <b>%v</b>. <b class=\"text-danger\">Неправильно</b>", tests + 1, answer)),
		})
		if err != nil {
			logrus.WithError(err).Errorf("Can't execute answer.html")
			return
		}
		return
	}

	if decision == "YES" {
		metrics.Success.Inc()

		err = tmpl.Execute(w, &Result{
			Tests:  template.HTML("100"),
			Answer: template.HTML(fmt.Sprintf(
				"Ура! Вот твой <s>Ыж</s> флаг: <b class=\"h4 text-success\">%v</b>",
				viper.GetString("FLAG"))),
		})
		if err != nil {
			logrus.WithError(err).Errorf("Can't execute answer.html")
			return
		}
		return
	}
}

