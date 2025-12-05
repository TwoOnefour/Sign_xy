package client

import (
	"net/url"
	"strings"
)

func PythonCompatibleEncode(str string) string {
	encoded := url.QueryEscape(str)
	encoded = strings.ReplaceAll(encoded, "+", "%20")
	encoded = strings.ReplaceAll(encoded, "%21", "!")
	encoded = strings.ReplaceAll(encoded, "%27", "'")
	encoded = strings.ReplaceAll(encoded, "%28", "(")
	encoded = strings.ReplaceAll(encoded, "%29", ")")
	encoded = strings.ReplaceAll(encoded, "%2A", "*")
	encoded = strings.ReplaceAll(encoded, "%7E", "~")
	encoded = strings.ReplaceAll(encoded, "%2E", ".")
	return encoded
}
