# Description
**由于我已经没有课了，不保证能用，可以先自己尝试使用**

**如果有学弟愿意维护，可以自行抓包，fork后提交pull request维护代码仓库，或者提issue，我会尽可能维护**

这是一个小雅刷课的python程序，分析了一天js，复现了登陆的密码加密，并且能实现刷课功能，~~目前手上只有武理的号~~ 老毕灯毕业后没号了，所以没办法做其他学校的

但是华师的多半可以（自信）

***如果觉得好用请点一个免费的star，这对我真的很重要***

# Configuration
## Install Module
```
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## Modify username and password
第一次登录的时候你需要输入你的账号密码，之后会保存到本地目录

username为学号，password为你的明文密码，有小雅自带的加密登录，~~武理跳转统一门户登录~~
# Usage
```
python ./main.py -t # 刷时长, 时长功能我记得是第二天才会统计，若刷完后第二天没有统计，请发issue
python ./main.py -f # 刷课
python ./main.py -h # 帮助
```
这个程序会在目录下生成一个Authorization.txt的文件用于存放token，同时会生成一个group_id.txt的文件，group_id.txt作为课程列表缓存，避免反复访问api，然后程序会遍历这些课程一个个签到

**注意，请在每个学期开始的时候清除目录下group_id.txt文件,否则将不会刷新课程**

# 更新日志
2024/11/29 更新了接口加密参数，详见`Signature.py`，目前`刷时长`和`武理的登陆模块`是正常使用的，其他功能不保证使用
![屏幕截图 2024-11-29 170612](https://github.com/user-attachments/assets/0920e3cd-0824-43dd-bcc0-556351058a8c)

2025/11/26 加密签名算法更新，目前刷课和小雅登录是没问题的

# TODO
- 使用go重构
# Disclaimer
此程序仅用于学习交流，如小雅方认为侵犯权益，请联系我，我会将其删除

