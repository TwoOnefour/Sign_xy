package model

import "time"

type Sign struct {
	r []string
}
type DefaultReq struct {
	Message   string `json:"message"`
	Signature string `json:"signature"`
	Timestamp string `json:"timestamp"`
	Nonce     string `json:"nonce"`
}

type SignOptions struct {
	TimeStamp time.Time `json:"timestamp"`
	Nonce     string    `json:"nonce"`
}
