package whut

import (
	"bytes"
	"crypto/sha1"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"github.com/google/uuid"
	"github.com/twoonefour/sign_xy/xy-go/internal/model"
	"github.com/twoonefour/sign_xy/xy-go/pkg/str"
	"log"
	"net/http"
	"net/url"
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

// 登陆
func (c *Client) login(clientId, schoolName, redirectUri string) (bool, error) {
	path := "/api/auth/login/loginByMobileOrAccount"
	req := c.rClient.R()
	_loginReq := loginReq{
		Account:     c.username,
		Password:    c.password,
		State:       str.RandomString(6),
		ClientId:    clientId,
		SchoolId:    schoolName,
		RedirectUri: redirectUri,
	}
	req.SetBody(_loginReq)
	var _loginResp loginResp
	req.SetResult(&_loginResp)
	_, err := req.Execute(http.MethodPost, path)
	if err != nil {
		return false, err
	}
	if _loginResp.Code != 200 || _loginResp.Data.Valid != true {
		return false, fmt.Errorf("getschool err: %s", _loginResp.Message)
	}
	var _listAccountsResp listAccountsResp
	if _, err := c.rClient.R().SetResult(&_listAccountsResp).Get("/api/auth/login/listAccounts?isVerifyAccount=true"); err != nil {
		return false, err
	} else if len(_listAccountsResp.Data.Accounts) == 0 {
		return false, fmt.Errorf("getAccount err: %s", _listAccountsResp.Message)
	}
	// 这下面不需要处理错误，因为上面已经都处理过了, 到这一步已经登陆成功了
	c.rClient.R().SetBody(map[string]string{
		"xyAccountId": _listAccountsResp.Data.Accounts[0].Id,
	}).Post("/api/auth/login/bySelectAccount")
	// WT-prd-access-token
	c.rClient.R().Get("/api/auth/oauth/onAccountAuthRedirect")
	c.rClient.SetBaseURL("https://whut.ai-augmented.com")
	tk := GetCookie(c.rClient.CookieJar().Cookies(&url.URL{Host: "ai-augmented.com", Scheme: "https"}), "WT-prd-access-token")
	c.rClient.SetHeader("Authorization", "Bearer "+tk)
	log.Println(c.getMe())
	return true, nil
}

// 个人信息，判断登陆成功的依据
func (c *Client) getMe() (string, error) {
	path := "/api/jw-starcmooc/user/currentUserInfo"
	base := "https://whut.ai-augmented.com"
	resp, err := c.rClient.R().Get(fmt.Sprintf("%s%s", base, path))
	return resp.String(), err
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

// groupid是课程信息，别问我为什么这样命名，他就是这样命名的
func (c *Client) getGroupId() ([]course, error) {
	path := "/api/jx-iresource/group/student/groups?time_flag=1"
	var courseResp listCourseResp
	if _, err := c.rClient.R().SetResult(&courseResp).Get(path); err != nil {
		return nil, nil
	}
	// 牛魔的这里又变成0是登陆成功了，上面又是200是登陆成功，老冯子没了？
	if courseResp.Code != 0 {
		return nil, fmt.Errorf("getCourse err: %s", courseResp.Message)
	}
	return courseResp.Data, nil
}

func (c *Client) SetRecord(courseId string) error {
	return nil
}

// 获取任务点信息，如每一个ppt 视频需要刷的任务点
func (c *Client) getTasks(courseId string) ([]tasks, error) {
	path := "/api/jx-stat/group/task/queryTaskNotices"
	req := c.rClient.R()
	req.SetQueryParams(map[string]string{
		"group_id": courseId,
		"role":     "1",
	})
	var _queryTasksResp queryTasksResp
	req.SetResult(&_queryTasksResp)
	_, err := req.Execute(http.MethodGet, path)
	if err != nil {
		return nil, err
	}
	return _queryTasksResp.Data.StudentTasks, nil
}
