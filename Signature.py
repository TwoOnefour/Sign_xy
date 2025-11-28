import hashlib
import uuid
import json
import time
import urllib.parse


def sign(query_body, nonce=None, timestamp=None):
    # 1. 处理 message: 模拟 JSON.stringify
    # 注意：Python 的 json.dumps 默认会有空格，而 JS 的 JSON.stringify 默认没有空格。
    # 这里必须使用 separators=(',', ':') 去除空格，否则签名会不一致。
    message_str = json.dumps(query_body, separators=(',', ':'), ensure_ascii=False)

    # 2. 生成 timestamp (毫秒级)
    if not timestamp:
        timestamp = str(int(time.time() * 1000))

    # 3. 生成 nonce
    if not nonce:
        nonce = str(uuid.uuid4())

    # 4. URL 编码 message
    # JS 的 encodeURIComponent 不转义: A-Z a-z 0-9 - _ . ! ~ * ' ( )
    # Python 的 quote 默认只保留 safe='/'。
    # 为了尽可能匹配 JS 的行为，我们需要指定 safe 参数。
    encoded_message = urllib.parse.quote(message_str, safe="~()*!.'")

    # 5. 构建待排序数组 r
    # 对应 JS: r.push("--xy-create-signature--")
    r = [
        encoded_message,
        timestamp,
        nonce,
        "--xy-create-signature--"
    ]

    # 6. 排序并拼接
    # 对应 JS: r.sort().join("")
    r.sort()
    raw_string = "".join(r)

    # 7. 计算 SHA1
    # 对应 JS: Tie.SHA1(...).toString()，通常 toString() 默认是 Hex 格式
    sha1 = hashlib.sha1()
    sha1.update(raw_string.encode('utf-8'))
    signature = sha1.hexdigest()

    return {
        "message": message_str,
        "signature": signature,
        "timestamp": timestamp,
        "nonce": nonce
    }
