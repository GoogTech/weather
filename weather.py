'''
Author: GoogTech
Date: 2020-12-20 11:08:38
LastEditTime: 2020-12-24 20:16:49
Description: Get Today Weather INFO Then Ouput Voice Prompt And Send It To Your WeChat
Version: v0.0.2
'''

import os
import urllib.parse
import urllib.request
import gzip
import json
import requests
import playsound
from aip import AipSpeech
import re
from config import *
from apscheduler.schedulers.blocking import BlockingScheduler


# 获取天气数据
def Get_weather_data():
    print('\n\n=============== 天气查询 ===============')
    # city_name = input('请输入要查询的城市名称: ')
    # url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + urllib.parse.quote(city_name)
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + urllib.parse.quote(
        "南京")
    weather_data = urllib.request.urlopen(url).read()
    # 读取网页数据
    weather_data = gzip.decompress(weather_data).decode('utf-8')
    # 解压网页数据
    weather_dict = json.loads(weather_data)
    return weather_dict


# 获取今日天气情况
def Show_weather(weather_data):
    weather_dict = weather_data
    # if weather_dict.get('desc') == 'invilad-citykey':
    #     print('你输入的城市有误或未收录该城市的天气, 请您重新输入...')
    # elif weather_dict.get('desc') == 'OK':
    if weather_dict.get('desc') == 'OK':
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
        # print('温馨提示: ', weather_dict.get('data').get('ganmao'))
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


# 获取明日天气情况( 代码有待重构哟 )
def Show_weather_tomorrow(weather_data):
    weather_dict = weather_data
    if weather_dict.get('desc') == 'OK':
        forecast = weather_dict.get('data').get('forecast')
        print('明天日期: ', forecast[1].get('date'))
        print('城市: ', weather_dict.get('data').get('city'))
        print('明天天气: ', forecast[1].get('type'))
        print('明天温度: ', weather_dict.get('data').get('wendu') + '℃ ')
        print('明天高温: ', forecast[1].get('high'))
        print('明天低温: ', forecast[1].get('low'))
        print(
            '明天风级: ', forecast[1].get('fengli').split('CDATA')[1].split(']')
            [0].split('[')[1])
        print('明天风向: ', forecast[1].get('fengxiang'))
        weather_forecast_tomorrow_txt = \
                    '您好,接下来播报的是明天的天气预报,您所在的城市是%s, ' \
                    '明天天气%s, ' \
                    '温度为%s, ' \
                    '最高温度为%s, ' \
                    '最低温度为%s, ' \
                    '风级为%s, ' \
                    '风向为%s, ' % \
                    (
                        weather_dict.get('data').get('city'),
                        forecast[1].get('type'),
                        weather_dict.get('data').get('wendu') + '℃ ',
                        forecast[1].get('high'),
                        forecast[1].get('low'),
                        forecast[1].get('fengli').split('CDATA')[1].split(']')[0].split('[')[1],
                        forecast[1].get('fengxiang'),
                    )
        return weather_forecast_tomorrow_txt


# 百度语音播报今天天气状况
def Voice_broadcast(weather_forcast_txt):
    weather_info = weather_forcast_txt
    # 将天气信息推送到微信
    if SendToWeChat(weather_forcast_txt):
        weather_info = weather_info + \
        '最后, 以上天气预报内容已通过「Server 酱」推送到了你的微信~'
    else:
        weather_info = weather_info + \
        '注意: 以上天气预报内容无法通过「Server 酱」推送到你的微信!'
    # 百度语音合成, 参数配置详见: https://ai.baidu.com/ai-doc/SPEECH/Qk38y8lrl
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(weather_info, 'zh', 1, {'vol': 5, 'per': 0})
    if not isinstance(result, dict):
        with open(BAIDU_TTS_MP3, 'wb') as f:
            f.write(result)
        f.close()
    # 使用 playsound 模块播放语音
    playsound.playsound(BAIDU_TTS_MP3)
    # 删除 BAIDU_TTS_MP3 文件, 防止 PermissionError: [Errno 13] Permission denied: '.tts.mp3'
    # refer to: https://www.it1352.com/1641930.html
    os.remove(BAIDU_TTS_MP3)


# 将获取的天气信息推送到微信
def SendToWeChat(weather_forecast_txt):
    # text 为推送的 title, desp 为推送的 description
    title = "天气预报来咯~"
    content = weather_forecast_txt
    data = {"text": title, "desp": content}
    # 发送( 同样内容的消息一分钟只能发送一次, 服务器只保留一周的消息记录 )
    return True if requests.post(SERVER_API,
                                 data=data).status_code == 200 else False


# 获取今日天气预报信息并播报
def run_today():
    weather_data = Get_weather_data()
    weather_forecast_txt = Show_weather(weather_data)
    Voice_broadcast(weather_forecast_txt)


# 获取明日天气预报信息并播报
def run_tomorrow():
    weather_data = Get_weather_data()
    weather_forecast_tomorrow_txt = Show_weather_tomorrow(weather_data)
    Voice_broadcast(weather_forecast_tomorrow_txt)


# 主函数
if __name__ == '__main__':
    scheduler = BlockingScheduler()
    # scheduler.add_job(run, 'interval', seconds = 90, id = 'job-one') # 每 90 秒执行一次,用于测试
    # scheduler.add_job(run, 'cron', hour='08-22', minute='10', second = '00', id = 'job-one')  # 每天 08:10:00 和 22:10:00 点分别执行一次
    scheduler.add_job(run_today,
                      'cron',
                      hour='08',
                      minute='10',
                      second='00',
                      id='job-today')
    scheduler.add_job(run_tomorrow,
                      'cron',
                      hour='22',
                      minute='10',
                      second='00',
                      id='job-tomorrow')
    scheduler.start()
