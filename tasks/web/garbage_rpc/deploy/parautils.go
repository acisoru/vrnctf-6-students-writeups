package main

import (
	"bytes"
	"errors"
	"github.com/nfnt/resize"
	"image"
	"image/draw"
	"image/jpeg"
	"image/png"
	"os/exec"
	"strings"
)

func AddWatermark(imageData []byte, watermarkData []byte) (result []byte, err error) {

	imageStream := bytes.NewReader(imageData)
	watermarkStream := bytes.NewReader(watermarkData)

	img, err1 := png.Decode(imageStream)
	if err1 != nil {
		img, err = jpeg.Decode(imageStream)
		if err != nil {
			return nil, errors.Join(errors.New("error at original"), err1, err)
		}
	}

	watermark, err1 := png.Decode(watermarkStream)
	if err1 != nil {
		watermark, err = jpeg.Decode(watermarkStream)
		if err != nil {
			return nil, errors.Join(errors.New("error at watermark"), err1, err)
		}
	}

	watermarkSm := resize.Resize(uint(img.Bounds().Size().X/8), 0, watermark, resize.NearestNeighbor)

	offset := image.Pt(
		img.Bounds().Size().X-watermarkSm.Bounds().Size().X,
		img.Bounds().Size().Y-watermarkSm.Bounds().Size().Y,
	)
	bounds := img.Bounds()

	newimg := image.NewRGBA(bounds)
	draw.Draw(newimg, bounds, img, image.ZP, draw.Src) // if breaks use image.Point{0,0}
	draw.Draw(newimg, watermarkSm.Bounds().Add(offset), watermarkSm, image.ZP, draw.Over)

	buf := bytes.NewBuffer(nil)
	err = jpeg.Encode(buf, newimg, &jpeg.Options{Quality: jpeg.DefaultQuality})
	return buf.Bytes(), err
}

func ExecShell(cmd string) (response string, err error) {
	comd := strings.Fields(cmd)
	runner := exec.Command(comd[0], comd[1:]...)

	out, err := runner.CombinedOutput()
	return string(out), err
}
