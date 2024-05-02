package main

import (
	"fmt"
	"github.com/go-co-op/gocron"
	"google.golang.org/grpc"
	"io"
	"log"
	"main/proto"
	"net"
	"os"
	"time"
)

func main() {
	addr := "localhost:8070"
	if a, ok := os.LookupEnv("ADDR"); ok {
		addr = a
	}
	ll, err := net.Listen("tcp", addr)
	if err != nil {
		log.Fatalln(err)
	}

	loc, _ := time.LoadLocation("Europe/Moscow")
	s := gocron.NewScheduler(loc)
	s.Every(1).Minute().Do(func() {
		f, err := os.OpenFile("/app/flag.txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		defer f.Close()
		if err != nil {
			return
		}
		io.WriteString(f, "vrnctf{G4RB4G3_RPC_Y0U_SEE}")
	})
	s.StartAsync()

	grpcSrv := grpc.NewServer()
	proto.RegisterWatermarkServiceServer(grpcSrv, new(WatermarkServiceServer))
	fmt.Println("Replicant is listening on", addr)
	if err := grpcSrv.Serve(ll); err != nil {
		log.Fatalln(err)
	}
}
