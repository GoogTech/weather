'''
Author: GoogTech
Date: 2020-12-20 11:08:38
LastEditTime: 2020-12-20 16:43:59
Description: Get Today Weather INFO Then Ouput Voice Prompt And Send It To Your WeChat
Version: v0.0.2
'''

import urllib.parse
import urllib.request
import gzip
import json
import requests
import playsound
from aip import AipSpeech
import re
from config import *


# 获取天气数据
def Get_weather_data():
    print('=============== 天气查询 ===============')
    city_name = input('请输入要查询的城市名称: ')
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + urllib.parse.quote(
        city_name)
    weather_data = urllib.request.urlopen(url).read()
    # 读取网页数据
    weather_data = gzip.decompress(weather_data).decode('utf-8')
    # 解压网页数据
    weather_dict = json.loads(weather_data)
    return weather_dict


# 获取天气情况
def Show_weather(weather_data):
    weather_dict = weather_data
    if weather_dict.get('desc') == 'invilad-citykey':
        print('你输入的城市有误或未收录该城市的天气, 请您重新输入...')
    elif weather_dict.get('desc') == 'OK':
        forecast = weather_dict.get('data').get('forecast')
        print('日期: ', forecast[0].get('date'))
        print('城市: ', weather_dict.get('data').get('city'))
        print('天气: ', forecast[0].get('type'))
        print('温度: ', weather_dict.get('data').get('wendu') + '℃ ')
        print('高温: ', forecast[0].get('high'))
        print('低温: ', forecast[0].get('low'))
        print(
            '风级: ', forecast[0].get('fengli').split('CDATA')[1].split(']')
            [0].split('[')[1])
        print('风向: ', forecast[0].get('fengxiang'))
        print('温馨提示: ', weather_dict.get('data').get('ganmao'))
        weather_forecast_txt = \
                    '您好,您所在的城市是%s, ' \
                    '天气%s, ' \
                    '当前温度为%s, ' \
                    '今天最高温度为%s, ' \
                    '最低温度为%s, ' \
                    '风级为%s, ' \
                    '风向为%s, ' \
                    '温馨提示: %s' % \
                    (
                      weather_dict.get('data').get('city'),
                      forecast[0].get('type'),
                      weather_dict.get('data').get('wendu') + '℃ ',
                      forecast[0].get('high'),
                      forecast[0].get('low'),
                      forecast[0].get('fengli').split('CDATA')[1].split(']')[0].split('[')[1],
                      forecast[0].get('fengxiang'),
                      weather_dict.get('data').get('ganmao')
                    )
        return weather_forecast_txt


# 百度语音播报今天天气状况
def Voice_broadcast(weather_forcast_txt):
    weather_forecast_txt = weather_forcast_txt
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    # 百度语音合成, 参数配置详见: https://ai.baidu.com/ai-doc/SPEECH/Qk38y8lrl
    result = client.synthesis(weather_forecast_txt, 'zh', 1, {
        'vol': 5,
        'per': 0
    })
    if not isinstance(result, dict):
        with open(BAIDU_TTS_MP3, 'wb') as f:
            f.write(result)
        f.close()
    # 使用 playsound 模块播放语音
    playsound.playsound(BAIDU_TTS_MP3)


# 将获取的天气信息推送到微信
def SendToWeChat(weather_forecast_txt):
    # text 为推送的 title, desp 为推送的 description
    title = "今日天气预报来咯~"
    content = weather_forecast_txt
    data = {"text": title, "desp": content}
    # 发送( 同样内容的消息一分钟只能发送一次, 服务器只保留一周的消息记录 )
    if requests.post(SERVER_API, data=data).status_code == 200:
        print("天气预报内容已通过「Server 酱」推送到了你的微信~")
    else:
        print("「Server 酱」推送消息失败 !")


# 主函数
if __name__ == '__main__':
    weather_data = Get_weather_data()
    weather_forecast_txt = Show_weather(weather_data)
    Voice_broadcast(weather_forecast_txt)
    SendToWeChat(weather_forecast_txt)
