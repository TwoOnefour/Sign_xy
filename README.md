# Description
这是一个小雅签到的python程序，分析了一天js，复现了登陆的密码加密，并且能实现简单的签到功能，目前手上只有武理的号，所以没办法做其他学校的

# Configuration
## Install Module
```
pip install -r requirements.txt -i https://pypi.tsinghua.edu.cn/simple
```
## Nodejs
你需要配置nodejs并将其放入系统环境变量中，nodejs请访问[官网](https://nodejs.cn/)下载

## Modify username and password
你需要在__init__中修改username和password

![图片](https://user-images.githubusercontent.com/77989499/229537712-9fc2ff19-7f53-4e32-92fd-018666ec2639.png)

username为学号，password为你的明文密码
# Usage
```
python ./main.py
```
这个指令会在目录下生成一个Authorization.txt的文件用于存放token，同时会生成一个group_ip.txt的文件，group_id.txt作为课程列表缓存，避免反复访问api，然后程序会遍历这些课程一个个签到

建议配合linux的crontab使用，在你经常需要打卡的课的时间段写下crontab命令

# Disclaimer
此程序仅用于学习交流，如认为侵犯权益，请联系我，我会将其删除
