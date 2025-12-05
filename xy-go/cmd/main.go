package cmd

import (
	"github.com/joho/godotenv"
	"github.com/twoonefour/sign_xy/xy-go/internal/client/whut"
	"github.com/twoonefour/sign_xy/xy-go/internal/service"
	"os"
)

func main() {
	err := godotenv.Load()
	if err != nil {
		panic("请在运行目录添加.env文件，填写环境变量XY_USERNAME和XY_PASSWORD")
	}
	XyUsername := os.Getenv("XY_USERNAME")
	XyPassword := os.Getenv("XY_PASSWORD")
	client := whut.NewClient(XyUsername, XyPassword)
	xy := service.NewXYService(client)
	xy.RecordLearning()
}
