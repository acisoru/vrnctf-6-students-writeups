package main

import (
	"encoding/json"
	"fmt"
	"github.com/gorilla/mux"
	"golang.org/x/exp/maps"
	"log"
	"net/http"
	"os"
	"os/signal"
	"strconv"
)

type HandlerContext struct {
	knyazya map[int]Knyaz
}

type Knyaz struct {
	Name string `json:"name"`
	Desc string `json:"desc"`
}

func main() {
	fmt.Println("Starting...")
	ctx := &HandlerContext{
		knyazya: map[int]Knyaz{
			0: {
				Name: "Святогор",
				Desc: "Киевский",
			},
			1: {
				Name: "Вольга",
				Desc: "Святославич",
			},
			2: {
				Name: "Микула",
				Desc: "Селянинович",
			},
			3: {
				Name: "Илья",
				Desc: "Муромец",
			},
			4: {
				Name: "Добрыня",
				Desc: "vrnctf{h3r3_1_f0und_th33}",
			},
			5: {
				Name: "Алёша",
				Desc: "Попович",
			},
		},
	}
	byIdPath := "/knyaz/{id:[-]?[0-9]+}"
	listPath := "/knyazya"
	router := mux.NewRouter()
	router.NewRoute().Methods(http.MethodGet).HandlerFunc(ctx.getByIdHandler).Path(byIdPath)
	router.NewRoute().Methods(http.MethodGet).HandlerFunc(ctx.getListHandler).Path(listPath)
	go func() {
		_ = http.ListenAndServe(":8080", router)
	}()
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)
	<-c
}

func (ctx *HandlerContext) getByIdHandler(w http.ResponseWriter, r *http.Request) {
	presentApp := r.Header.Get("App-ID")
	if len(presentApp) == 0 {
		w.WriteHeader(http.StatusBadRequest)
		fmt.Println("1")
		return
	}
	presentBearer := r.Header.Get("Authorization")
	if len(presentBearer) == 0 {
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	vars := mux.Vars(r)
	mapId, _ := strconv.Atoi(vars["id"])
	valInMap, ok := ctx.knyazya[mapId]
	if !ok {
		w.WriteHeader(http.StatusNotFound)
		return
	}
	marshalled, err := json.Marshal(valInMap)
	_, err = fmt.Fprintf(w, "%s", marshalled)
	if err != nil {
		log.Fatal("Failed to write response: ", err)
		return
	}
}

func (ctx *HandlerContext) getListHandler(w http.ResponseWriter, r *http.Request) {
	presentApp := r.Header.Get("app-id")
	if len(presentApp) == 0 {
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	presentBearer := r.Header.Get("authorization")
	if len(presentBearer) == 0 {
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	marshalled, err := json.Marshal(maps.Keys(ctx.knyazya))
	_, err = fmt.Fprintf(w, "%s", marshalled)
	if err != nil {
		log.Fatal("Failed to write response: ", err)
		return
	}
}
