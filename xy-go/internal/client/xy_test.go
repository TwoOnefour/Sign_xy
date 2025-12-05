package client

import (
	"github.com/twoonefour/sign_xy/xy-go/internal/model"
	"log"
	"testing"
	"time"
)

func Test_XY(T *testing.T) {
	c := time.UnixMilli(1764919515201)
	xy := NewClient("xxx", "xxx")
	sign, err := xy.Sign("{'123':'43123'}", model.SignOptions{Nonce: "427f7e23-cd53-4df8-93b9-749ffe439a48", TimeStamp: c})
	if err != nil {
		return
	}
	log.Println(sign)
	xy.login("xy_client_whut", "d447ffa6-0679-4bb2-a522-db24dc0e0b3d", "https://whut.ai-augmented.com/api/jw-starcmooc/user/authorCallback?cb=https://whut.ai-augmented.com/app/jx-web/mycourse")
}
