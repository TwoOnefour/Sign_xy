package client

import (
	"bytes"
	"crypto/sha1"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"github.com/google/uuid"
	"github.com/twoonefour/sign_xy/xy-go/internal/model"
	"github.com/twoonefour/sign_xy/xy-go/pkg/str"
	"net/http"
	"resty.dev/v3"
	"slices"
	"strconv"
	"strings"
	"time"
)

type Client struct {
	username   string
	password   string
	rClient    *resty.Client
	schoolMap  map[string]school
	schoolList []string
}

func NewClient(username, password string) *Client {
	rClient := resty.New()
	rClient.SetTimeout(10 * time.Second)
	rClient.SetHeaders(map[string]string{
		"Content-Type":                 "application/json; charset=utf-8",
		"access-control-allow-methods": "GET,POST,OPTIONS",
		"Accept-Encoding":              "gzip, deflate, br",
		"Connection":                   "keep-alive",
		"If-None-Match":                "W/47-Gkgd+hPnYQ+HOAd1+Mgij152K58",
		"Accept":                       "*/*",
		"User-Agent":                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
		"Accept-Language":              "en-US,en;q=0.9",
		"Access-Control-Allow-Origin":  "*",
	})
	rClient.SetBaseURL("https://infra.ai-augmented.com")
	rClient.SetProxy("http://127.0.0.1:9099")
	client := &Client{
		username: username,
		password: password,
		rClient:  rClient,
	}
	_schoolMap := make(map[string]school)
	_schoolList := make([]string, 0)
	whutSchoolInfo, err := client.getSchools(whut.String())
	if err != nil {
		return nil
	}
	if len(whutSchoolInfo) > 0 {
		_schoolMap[whutSchoolInfo[0].DisplayName] = whutSchoolInfo[0]
		_schoolList = append(_schoolList, whutSchoolInfo[0].DisplayName)
	}
	ccnuSchoolInfo, err := client.getSchools(ccnu.String())
	if err != nil {
		return nil
	}
	for _, _school := range ccnuSchoolInfo {
		_schoolMap[_school.DisplayName] = _school
		_schoolList = append(_schoolList, _school.DisplayName)
	}
	client.schoolMap = _schoolMap
	client.schoolList = _schoolList
	return client
}

func (c *Client) Sign(queryBody interface{}, options ...model.SignOptions) (*model.DefaultReq, error) {
	buffer := &bytes.Buffer{}
	encoder := json.NewEncoder(buffer)
	encoder.SetEscapeHTML(false)
	err := encoder.Encode(queryBody)
	if err != nil {
		return nil, err
	}
	messageStr := strings.TrimSuffix(buffer.String(), "\n")
	var timeStamp time.Time
	var nonce string
	if len(options) > 0 {
		timeStamp = options[0].TimeStamp
		nonce = options[0].Nonce
	}
	if timeStamp.IsZero() {
		timeStamp = time.Now()
	}
	if nonce == "" {
		nonce = uuid.New().String()
	}

	timeStampStr := strconv.FormatInt(timeStamp.UnixMilli(), 10)

	encodedMsg := PythonCompatibleEncode(messageStr)

	r := []string{
		encodedMsg,
		timeStampStr,
		nonce,
		"--xy-create-signature--",
	}
	slices.Sort(r)

	rawStr := strings.Join(r, "")

	h := sha1.New()
	h.Write([]byte(rawStr))
	signature := hex.EncodeToString(h.Sum(nil))
	return &model.DefaultReq{
		Message:   messageStr,
		Nonce:     nonce,
		Timestamp: timeStampStr,
		Signature: signature,
	}, nil
}

func (c *Client) login(clientId, schoolName, redirectyUri string) (bool, error) {
	path := "/api/auth/login/loginByMobileOrAccount"
	req := c.rClient.R()
	_loginReq := loginReq{
		Account:     c.username,
		Password:    c.password,
		State:       str.RandomString(6),
		ClientId:    clientId,
		SchoolId:    schoolName,
		RedirectUri: redirectyUri,
	}
	req.SetBody(_loginReq)
	var _loginResp loginResp
	req.SetResult(&_loginResp)
	_, err := req.Execute("POST", path)
	if err != nil {
		return false, err
	}
	if _loginResp.Code != 200 || _loginResp.Data.Valid != true {
		return false, fmt.Errorf("getschool err: %s", _loginResp.Message)
	}
	var _listAccountsResp listAccountsResp
	c.rClient.R().SetResult(&_listAccountsResp).Get("/api/auth/login/listAccounts?isVerifyAccount=true")
	c.rClient.R().SetBody(map[string]string{
		"xyAccountId": _listAccountsResp.Data.Accounts[0].Id,
	}).Post("/api/auth/login/bySelectAccount")
	c.rClient.R().Get("/api/auth/oauth/onAccountAuthRedirect")
	return true, nil
}

func (c *Client) getSchools(clientId string) ([]school, error) {
	req := c.rClient.R()
	req.SetQueryParam("clientId", clientId)
	var _schoolsResp schoolsResp
	req.SetResult(&_schoolsResp)
	_, err := req.Execute(http.MethodGet, "/api/auth/login/listSchoolsByClient")
	if err != nil {
		return nil, err
	}
	if _schoolsResp.Code != 200 {
		return nil, fmt.Errorf("getschool err: %s", _schoolsResp.Message)
	}

	return _schoolsResp.Data.School, nil
}
