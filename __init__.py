import requests
import os
import json
import time
import datetime
from Crypto.Cipher import DES
import base64
from lxml import etree
from enc import *


class Sign_xy:
    def __init__(self):
        # urllib3.disable_warnings()
        self.server_chan_apikey = ""  # server酱的apikey
        self.type = None
        self.webdriver = None
        self.times = None
        self.authorization = ""
        # self.sys = None
        self.node_path = None
        self.relogin = False
        self.headers = {
            "schoolcertify": "",  # 学校对应代码
            "Host": "ccnu.ai-augmented.com",
            "Content-Type": "application/json; charset=utf-8",
            "access-control-allow-methods": "GET,POST,OPTIONS",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "If-None-Match": "W/47-Gkgd+hPnYQ+HOAd1+Mgij152K58",
            "Accept": "*/*",
            "User-Agent": "xiaoya_mobile",
            "Authorization": self.authorization,
            "Accept-Language": "en-US,en;q=0.9",
            "Access-Control-Allow-Origin": "*",
        }
        self.url = "https://{}".format(self.headers["Host"])
        self.sessions = requests.Session()
        self.account = {
            "username": "",
            "password": ""
        }
        self.pattern = ""
        if os.path.exists(os.path.split(os.path.realpath(__file__))[0] + "/account.txt"):
            with open(os.path.split(os.path.realpath(__file__))[0] + "/account.txt", "r") as f:
                account_list = f.readlines()
                self.account["username"] = account_list[0].strip("\n").strip(" ")
                self.account["password"] = account_list[1].strip("\n").strip(" ")
                self.headers["schoolcertify"] = account_list[2].strip("\n").strip(" ")
                self.pattern = account_list[3].strip("\n").strip(" ")

    def encrypt(self, data):  # 小雅自带的加密
        bs = 8
        password = "bbd92272a179a2db46ee01aed4df8cda".encode("utf-8")[:8]
        iv = "12345678".encode("utf-8")
        pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
        cipher = DES.new(password, DES.MODE_CBC, iv)
        return base64.b64encode(cipher.encrypt(pad(data).encode())).decode("utf-8")

    def whut_login(self, service, username, password):  # 门户登录的逻辑
        self.sessions.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
        })
        html = self.sessions.get("http://zhlgd.whut.edu.cn/tpass/login", params={
            "service": service
        })
        etree.HTMLParser(encoding="utf-8")
        # tree = etree.parse(local_file_path)
        tree = etree.HTML(html._content.decode("utf-8"))
        tpass = dict(tree.xpath('//*[@id="lt"]')[0].attrib)["value"]
        # des = strEnc(self.account["username"] + self.account["password"] + tpass, "1", "2", "3")
        self.sessions.headers.update({})
        self.sessions.cookies.set(domain="whut.edu.cn", path="/", name="cas_hash", value="")
        # print(tpass)
        result = self.sessions.post(
            url="http://zhlgd.whut.edu.cn/tpass/login",
            params={
                "service": service
            },
            data={
                "rsa": "",
                "ul": encrypt(username),
                "pl": encrypt(password),
                "lt": tpass,
                "execution": "e1s1",
                "_eventId": "submit",
            }, verify=False, allow_redirects=False)
        if result.headers.get("location") is None:
            return False
        return result.headers["location"]

    def login(self):  # 登陆主函数
        if os.path.exists(os.path.split(os.path.realpath(__file__))[0] + "/authorization.txt"):  # 如果有登录信息，直接使用
            print("Cookies exists. Try to login by using cookies.")
            with open(os.path.split(os.path.realpath(__file__))[0] + "/authorization.txt", "r") as f:
                self.headers["Authorization"] = f.readline().strip("\n")
            self.sessions.headers.update(self.headers)
            # self.sessions.get("{}/api")
            # self.getUserInfo()
            result = json.loads(self.getUserInfo().text)
            if result["code"] != 200: # cookie过期
                print("Cookies has expired. Sign in automatically.")
                self.relogin = True
                os.remove("./authorization.txt")
                return False
            self.login_success()

        else:
            print("Try to login by username and password")
            if self.headers["schoolcertify"] == "":
                while True:
                    self.headers["schoolcertify"] = input("输入登录学校，1为华师，2为武理：")
                    if self.headers["schoolcertify"] == "1":
                        self.headers["schoolcertify"] = "10511"
                        self.pattern = "2"
                    elif self.headers["schoolcertify"] == "2":
                        self.headers["schoolcertify"] = "10497"
                    else:
                        print("输入错误，请重新输入")
                        continue
                    break
            if self.headers["schoolcertify"] == "10497" and not self.relogin and self.pattern == "":
                self.pattern = input("输入登录方式，1为门户登录（门户登录不会挤掉客户端，推荐，如果是门户登录将永久签到），2为小雅直接登录：")
            if self.account["username"] == "" or self.account["password"] == "":
                    print("请填入账号密码。注意：账号密码为你统一身份认证的账号密码")
                    self.account["username"] = input("学号：")
                    self.account["password"] = input("密码：")
            if self.pattern == "1":  # 门户登录
                self.sessions.cookies.clear()
                url = self.whut_login("https://whut.ai-augmented.com/api/jw-starcmooc/user/cas/login?schoolCertify=10497", self.account["username"], self.account["password"])
                result1 = self.sessions.get(url, verify=False)
                self.headers["Authorization"] = f'Bearer {self.sessions.cookies.get("HS-prd-access-token")}'
                self.sessions.headers.update(self.headers)
                self.login_success()
                return True
            password = self.encrypt(self.account["password"])  # 密码加密
            self.sessions.headers.update(self.headers)
            result = self.sessions.post(
                "https://{}/api/jw-starcmooc/user/unifiedCheckLogin".format(self.headers["Host"]), verify=False, json={
                    "password": password,
                    "loginName": self.account["username"]
                }, headers=self.headers)
            if result.json().get("result") is None: # 如果登陆失败返回False
                return False
            token = json.loads(result.text)["result"]["token"]
            self.headers["Authorization"] = "Bearer {}".format(token) # 设置cookie
            self.sessions.headers.update(self.headers)
            self.login_success()
        return True

    def login_success(self):  # 登录成功后执行的函数 保存cookie和用户账号密码信息，输出信息到控制台
        with open(os.path.split(os.path.realpath(__file__))[0] + "/authorization.txt", "w") as f:
            f.write(self.headers["Authorization"])
        userinfo = json.loads(self.getUserInfo().text)
        realname = userinfo["result"]["realname"]
        # signInfo = userinfo["result"]["sign"]  # 可能是签到信息，暂且留空,不用留空。2023.05.16 证明为有签到任务也不存在此数据
        print("Login successfully. Welcome, {}".format(realname))
        self.relogin = False
        if os.path.exists(os.path.split(os.path.realpath(__file__))[0] + "/account.txt"):
            return
        with open(os.path.split(os.path.realpath(__file__))[0] + "/account.txt", "w") as f:
            f.write(self.account["username"] + "\n" + self.account["password"] + "\n" + self.headers[
                "schoolcertify"] + "\n" + self.pattern + "\n")

    def getUserInfo(self):  # 查看用户信息
        return self.sessions.get("https://{}/api/jw-starcmooc/user/currentUserInfo".format(self.headers["Host"]),
                                 verify=False)

    def get_cookie_status(self):  # 判断cookie是否过期
        if self.getUserInfo().json()["code"] == 401:
            try:
                print("Cookies has expired. Sign in automatically.")
                os.remove("./authorization.txt")
                self.relogin = True
            except Exception as e:
                print(e)
            while True:
                if self.login():
                    break

    def sign(self):  # 签到函数
        if not self.times:
            self.times = 1
        else:
            self.times = int(self.times)
        if self.pattern == "1":
            self.times = True
        count = 0 # 用于记录循环次数
        while self.times or count < self.times:
            self.get_cookie_status()  # 查看cookie状况，如果过期重新登陆
            for i in self.getGroup_id():  # 暂且写为所有课程都签到一遍
                # self.get_open_course(i.strip("\n"))["data"]
                # self.getRegister_id(i)
                result = self.getRegister_id(i.strip("\n"))

                if result["data"]["signing_register"]:
                    print(result)
                    result1 = self.sessions.post(
                        "https://{}/api/jx-iresource/register/sign".format(self.headers["Host"]), json={
                            "check_type": "1",
                            "register_id": result["data"]["signing_register"][0]["id"]
                        }, verify=False)
                    result1 = json.loads(result1.text)
                    print(result1)
                    if result1["code"] == 0:
                        msg = "{}   {}签到成功".format(str(datetime.datetime.now())[0:-7], result["data"]["group_name"])
                    elif result1["code"] == 50011:
                        msg = "{}   {}已经签到过了".format(str(datetime.datetime.now())[0:-7], result["data"]["group_name"])
                        print(msg)
                        time.sleep(60 * 90)  # 如果签到过了暂停90分钟签到
                        continue
                    else:
                        msg = "{}   {}{}".format(str(datetime.datetime.now())[0:-7], result["data"]["group_name"],
                                                 result1["message"])
                        time.sleep(60 * 90)  # 如果签到过了暂停90分钟签到
                    print(msg)
                    requests.get(f"https://sctapi.ftqq.com/{self.server_chan_apikey}.send?title={msg}")
                    if self.pattern != "1":
                        return
            time.sleep(60)  # 不建议改动
            count += 1

            # else:
            #     print("此课程不需要签到")

    def getRegister_id(self, group_id):  # 获取签到id
        return json.loads(self.sessions.get(
            "https://{}/api/jx-iresource/course/getOpenCourse?group_id={}&is_in_course=2".format(self.headers["Host"],
                                                                                                 group_id),
            verify=False).text)

    def get_tasks(self, group_id):  # 获取作业信息
        result = self.sessions.get("https://ccnu.ai-augmented.com/api/jx-stat/group/task/queryTaskNotices", params={
            "group_id": group_id,
            "role": 1
        })
        return json.loads(result.text)["data"]["student_tasks"]

    def finish_media(self):  # 完成视频 or 音频作业函数
        try:
            count = 0
            for j in self.getGroup_id():
                tasks = self.get_tasks(j.strip("\n"))
                for i in tasks:
                    if i["task_type"] == 1 and i["finish"] == 0:
                        # result = self.sessions.get("https://ccnu.ai-augmented.com/api/jx-iresource/vod/duration/{}".format(i["quote_id"])).text
                        # result = json.loads(result)
                        # if result["code"] == 60009:
                        #     # result = self.sessions.post("https://ccnu.ai-augmented.com/api/jx-iresource/vod/duration/{}".format(i["quote_id"]), json={
                        #     # "media_type": 1,  # 类型为录音
                        #     # "duration": 1,  # 总时间
                        #     # "played": 1,  # 播放次数
                        #     # "watched_duration": 1  # 已经看过的时长
                        #     # })  # 先请求一次获得duration,但是他好像没对这里做duration鉴权，duration为1返回的数据也是1，导致可以不用先请求 ps: 也许存在sql注入？
                        #     result = json.loads(result.text)
                        # result = result["data"]
                        # watched_duration = max(0, float(result["duration"]) - float(result["watched_duration"]) + 1)
                        self.sessions.post(
                            "https://ccnu.ai-augmented.com/api/jx-iresource/vod/duration/{}".format(i["quote_id"]),
                            json={
                                "media_type": 1,  # 类型为录音, 可以乱填
                                "duration": 100,  # 总时间，建议200-300
                                "played": 1,  # 播放次数
                                "watched_duration": 200  # 已经看过的时长
                            })
                        result = self.sessions.post(
                            "https://ccnu.ai-augmented.com/api/jx-iresource/vod/checkTaskStatus", json={
                                "task_id": i["task_id"],
                                "media_id": i["quote_id"],
                                "assign_id": i["assign_id"],
                                "group_id": i["group_id"]
                            })
                        count += 1
            print(f"完成了{count}个作业")
        except Exception as e:
            print(str(type(e)) + ":" + str(e))

    def get_open_course(self, group_id):  # 获取签到的课程信息
        result = self.sessions.get(f'https://{self.headers["Host"]}/api/jx-iresource/course/getOpenCourse', params={
            "group_id": group_id,
        })
        return result.json()

    def getGroup_id(self):  # 获取group_id
        if os.path.exists(os.path.split(os.path.realpath(__file__))[0] + "/group_id.txt"):
            with open(os.path.split(os.path.realpath(__file__))[0] + "/group_id.txt", "r") as f:
                result = f.readlines()
        else:
            result = json.loads(self.sessions.get(
                "https://{}/api/jx-iresource/group/student/groups?time_flag=1".format(self.headers["Host"]),
                verify=False).text)["data"]
            tmp = []
            for i in result:
                tmp.append(i["id"])
            with open(os.path.split(os.path.realpath(__file__))[0] + "/group_id.txt", "w") as f:
                f.write("\n".join(tmp))
            return tmp
        # if os.path.exists("./group_id.txt"):
        return result

    def run(self):  # 程序入口函数
        if not self.type:
            return
        while True:
            if self.login():
                break
            if not self.relogin:
                print("登陆失败，请确认登陆模式和账号密码")
                self.account["username"] = ""

        if self.type == "刷课":
            self.finish_media()  # 自动刷课，刷视频接口
        elif self.type == "签到":
            self.sign()
