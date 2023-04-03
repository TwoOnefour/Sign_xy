import requests
import urllib3
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import execjs
import json
import urllib3

class Sign_xy:
    def __init__(self):
        # urllib3.disable_warnings()
        self.webdriver = None
        self.authorization = ""
        self.headers = {
            "schoolcertify":"10497", # 学校对应代码
            "Host":"ccnu.ai-augmented.com",
            "Content-Type":"application/json; charset=utf-8",
            "access-control-allow-methods":"GET,POST,OPTIONS",
            "Accept-Encoding":"gzip, deflate, br",
            "Connection":"keep-alive",
            "If-None-Match":"W/47-Gkgd+hPnYQ+HOAd1+Mgij152K58",
            "Accept":"*/*",
            "User-Agent":"xiaoya_mobile",
            "Authorization":self.authorization,
            "Accept-Language":"en-US,en;q=0.9",
            "Access-Control-Allow-Origin":"*",
        }
        self.url = "https://{}".format(self.headers["Host"])
        self.sessions = requests.Session()
        self.account = {
            "username": "",  # 填入你自己的学号
            "password": ""  # 填入你自己的密码
        }

    def login(self):
        if os.path.exists("./authrization.txt"):
            print("Cookies exists. Try to login by using cookies")
            with open("./authrization.txt", "r") as f:
                self.headers["Authorization"] = "Bearer " + f.readline().strip("\n")
            self.sessions.headers.update(self.headers)
            # self.sessions.get("{}/api")
            # self.getUserInfo()

        else:
            print("Cookies don't exist. Try to login by username and password")
            node = execjs.get()
            with open("./Algorithm.js", encoding="UTF-8") as f:
                cxk = node.compile(f.read())
            funName = "crack"
            password = cxk.call(funName, self.account["password"])
            # self.headers.pop("Authorization")
            result = self.sessions.post("https://{}/api/jw-starcmooc/user/unifiedCheckLogin".format(self.headers["Host"]), verify=False, json={
                "password":password,
                "loginName":self.account["username"]
            },headers=self.headers)
            token = json.loads(result.text)["result"]["token"]
            with open("./authorization.txt", "w") as f:
                f.write(token)
            self.headers["Authorization"] = "Bearer {}".format(token)
            self.sessions.headers.update(self.headers)
            # print(1)
            userinfo = json.loads(self.getUserInfo().text)
            realname = userinfo["result"]["realname"]
            signInfo = userinfo["result"]["sign"]  # 可能是签到信息，暂且留空
        print("成功登录，欢迎你，{}".format(realname))
        # for i in group_id["data"]:
            # print(i["id"]) 所有课程id
        # print(1)

    def getUserInfo(self):
        return self.sessions.get("https://{}/api/jw-starcmooc/user/currentUserInfo".format(self.headers["Host"]))

    def sign(self, register_id):
        for i in register_id:  # 暂且写为所有课程都签到一遍
            self.sessions.post("https://{}/api/jx-iresource/register/sign".format(self.headers["Host"]), json={
                "check_type": "1",
                "register_id": i.strip("\n")
            }, verify=False)

    def getRegister_id(self, group_id):
        return json.loads(self.sessions.get(
            "https://{}/api/jx-iresource/course/getOpenCourse?group_id={}&is_in_course=2".format(self.headers["Host"],
                group_id), verify=False).text)

    def getGroup_id(self):
        if os.path.exists("./group_id.txt"):
            with open("./group_id.txt", "r") as f:
                result = f.readlines()
        else:
            result = json.loads(self.sessions.get("https://{}/api/jx-iresource/group/student/groups?time_flag=1".format(self.headers["Host"])).text)["data"]
            tmp = []
            for i in result:
                tmp.append(i["id"])
            with open("./group_id.txt", "w") as f:
                f.write("\n".join(tmp))
            return tmp
        # if os.path.exists("./group_id.txt"):
        return result

    def run(self):
        self.login()
        self.sign(self.getGroup_id())
