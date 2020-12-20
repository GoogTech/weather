import requests
from config import *

title = "今日天气预报来咯~"
content = """
你好鸭! 这是天气预报的内容...
"""
# text 为推送的 title, desp 为推送的 description
data = {"text": title, "desp": content}
# 发送
if requests.post(SERVER_API, data=data).status_code == 200:
    print("天气预报内容已通过「Server 酱」推送给了你的微信~")
else:
    print("「Server 酱」推送消息失败 !")
