import urllib3
from __init__ import Sign_xy
import sys
import zipfile
import os
import requests
import platform
import tarfile

if __name__ == "__main__":
    urllib3.disable_warnings()
    type = None
    tmp = sys.argv
    times = None
    system_ver = platform.system()
    if system_ver == "Windows":
        node_path = "/node-v16.19.1-win-x64/node.exe"
    else:
        node_path = "/node-v16.19.1-linux-x64/bin/node"
    if not os.path.exists(os.path.split(os.path.realpath(__file__))[0] + node_path):
        print("第一次运行，正在下载node")
        try:
            if system_ver == "Windows":
                file = requests.get("https://registry.npmmirror.com/-/binary/node/v16.19.1/node-v16.19.1-win-x64.zip")
                with open(os.path.split(os.path.realpath(__file__))[0] + "/node.zip", "wb") as f:
                    f.write(file.content)
                print("下载完成")
                file = zipfile.ZipFile(os.path.split(os.path.realpath(__file__))[0] + "/node.zip")
                file.extractall(os.path.split(os.path.realpath(__file__))[0])
                print("解压完成")
                file.close()
            elif system_ver == "Linux":
                file = requests.get("https://registry.npmmirror.com/-/binary/node/v16.19.1/node-v16.19.1-linux-x64.tar.gz")
                with open(os.path.split(os.path.realpath(__file__))[0] + "/node.tar.gz", "wb") as f:
                    f.write(file.content)
                print("下载完成")
                file = tarfile.open(os.path.split(os.path.realpath(__file__))[0] + "/node.tar.gz")
                file.extractall(os.path.split(os.path.realpath(__file__))[0])
                print("解压完成")
                file.close()
        except Exception as e:
            print("下载失败")
            sys.exit(0)
    if len(tmp) == 1 or tmp[1] == "-h":
        print("用法：\npython3 main.py -s\t\t签到,如果后面跟数字，那么会每隔1分钟签到一次，持续你给定的次数停止\npython3 main.py -f\t\t刷视频或者音频等作业\npython3 main.py -h\t\t返回此帮助")
    elif sys.argv[1].strip(" ") == "-s":
        type = "签到"
        if len(tmp) == 3:
            times = sys.argv[2]
    elif sys.argv[1].strip(" ") == "-f":
        type = "刷课"
    else:
        print(
            "用法：\npython3 main.py -s\t\t签到,如果后面跟数字，那么会每隔1分钟签到一次，持续你给定的次数停止\npython3 main.py -f\t\t刷视频或者音频等作业\npython3 main.py -h\t\t返回此帮助")

    mybot = Sign_xy()
    mybot.type = type
    mybot.times = times
    mybot.node_path = node_path
    mybot.run()
