'''
Author: GoogTech
Date: 2020-12-24 15:21:51
LastEditTime: 2020-12-24 18:31:12
Description: Transform The Voice To Text By Baidu AipSpeech
'''
from aip import AipSpeech
from config import *
import os

# 创建一个 AipSpeech
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 读取文件
def getfContent(fileName):
    with open(fileName, 'rb') as f:
        return f.read()


# 语音识别
def stt(fileName):
    # dev_pid 参数表示识别的语言类型, 1537表示中文普通话,
    # 更多详见文档: https://ai.baidu.com/ai-doc/SPEECH/Ek39uxgre
    result = client.asr(getfContent(fileName), 'wav', 16000, {
        'lan': 'zh',
    })
    print('result: %s', result)
    # 解析返回值, 打印语音识别的结果
    if result['err_msg'] == 'success.':
        word = result['result'][0]
        print("result: ", word)
    else:
        print("识别失败 !")


# Test
if __name__ == "__main__":
    # 识别 16k.wav 较准确
    stt('16k.wav')
