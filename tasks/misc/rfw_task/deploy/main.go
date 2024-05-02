package main

import (
	"fmt"
	"github.com/gorilla/mux"
	"io"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"strings"
)

type HandlerContext struct {
	Lizards []string
}

func main() {
	ctx := &HandlerContext{
		Lizards: []string{
			"First",
			"Second",
			"Third",
			"Fourth",
			"Fifth",
			"Sixth",
			"Seventh",
			"Eighth",
			"vrnctf{y2sher1_et0_5er10zn0}",
		},
	}
	pathString := "/{id:[-]?[0-9]+}"
	router := mux.NewRouter()
	router.NewRoute().Methods(http.MethodPost).HandlerFunc(ctx.getCard).Path(pathString)
	go func() {
		_ = http.ListenAndServe(":8080", router)
	}()
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)
	<-c
}

func (ctx *HandlerContext) getCard(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id, _ := strconv.Atoi(vars["id"])
	if id > 6 || id < 0 {
		w.WriteHeader(http.StatusForbidden)
		_, _ = w.Write([]byte("import core.widgets;\nwidget root = Text(text: \"Ошибка!\", textDirection: \"ltr\");"))
		return
	}
	body, err := io.ReadAll(r.Body)
	var str = string(body)
	var offset = 0
	var count = strings.Count(str, "XX")
	for i := 0; i < count; i++ {
		if id+offset > len(ctx.Lizards) {
			break
		}
		if id+offset >= len(ctx.Lizards) {
			w.WriteHeader(http.StatusBadRequest)
			return
		}
		str = strings.Replace(str, "XX", ctx.Lizards[id+offset], 1)
		offset++
	}
	_, err = fmt.Fprint(w, str)

	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
	}
}
