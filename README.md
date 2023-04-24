# Description
这是一个小雅签到的python程序，分析了一天js，复现了登陆的密码加密，并且能实现简单的签到功能，目前手上只有武理的号，所以没办法做其他学校的

但是华师的多半可以（自信）

***如果觉得好用请点一个免费的star，这对我真的很重要***

# Configuration
## Install Module
```
pip install -r requirements.txt -i https://pypi.tsinghua.edu.cn/simple
```

## Modify username and password
第一次登录的时候你需要输入你的账号密码，之后会保存到本地目录

username为学号，password为你的明文密码，目前实现的是统一门户登录
# Usage
```
python ./main.py -s 签到，如果后面跟着数字n，那么将会持续n次，间隔60秒签到
python ./main.py -t 刷课
python ./main.py -h 帮助
```
这个程序会在目录下生成一个Authorization.txt的文件用于存放token，同时会生成一个group_id.txt的文件，group_id.txt作为课程列表缓存，避免反复访问api，然后程序会遍历这些课程一个个签到

建议配合linux的crontab使用，在你经常需要打卡的课的时间段写下crontab命令

# Disclaimer
此程序仅用于学习交流，如认为侵犯权益，请联系我，我会将其删除
