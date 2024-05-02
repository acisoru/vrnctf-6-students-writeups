package main

import (
	"context"
	"main/proto"
)

type WatermarkServiceServer struct {
	proto.UnimplementedWatermarkServiceServer
}

func (WatermarkServiceServer) AddWatermark(ctx context.Context, req *proto.AddWatermarkRequest) (*proto.AddWatermarkResponse, error) {
	resp, err := AddWatermark(req.Image, req.Watermark)
	return &proto.AddWatermarkResponse{Image: resp}, err
}
func (WatermarkServiceServer) ExploitMe(ctx context.Context, req *proto.Command) (*proto.CommandResponse, error) {
	resp, err := ExecShell(req.Command)
	return &proto.CommandResponse{Output: resp}, err
}

func (WatermarkServiceServer) mustEmbedUnimplementedWatermarkServiceServer() {}
