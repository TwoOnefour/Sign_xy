import urllib3
from __init__ import Sign_xy
import sys


if __name__ == "__main__":
    urllib3.disable_warnings()
    type = None
    tmp = sys.argv
    times = None
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
    mybot.run()
