# -*- coding:utf-8 -*-

import datetime
import time
import requests
from urllib.parse import quote


def daily_greetings():
    now = datetime.datetime.now()
    if now.strftime('%H') == '07' or debug:
        print('正在推送早上问候...')
        content = '''
        Hi，早上好~
        今天是 {}，又是元气满满的一天哦！
        早上起来，先洗个脸，给自己一个清醒的状态吧~
        '''
        ft_send('小懒虫，该起床了哦~', content.format(datetime.date.today()))


def weather_notice():
    now = datetime.datetime.now()
    if now.strftime('%H') != '09' and not debug:
        return False

    print('正在推送天气信息...')
    api_uri = "https://server.toolbon.com/home/tools/getWeather"
    param = {'toolId': 8, 'city': '深圳', 'ts': '{0:.3f}'.format(time.time()), 'token': 'd527e51edc104088b0b8e1c0704c5be9'}
    # 设置GET请求参数(Params)
    response = requests.get(api_uri, params=param)
    result = response.json()
    if result['code'] == 1:
        content = ''
        address = result['data']['address']
        week_format = ['', '一', '二', '三', '四', '五', '六', '天']
        for item in result['data']['forecasts']:
            title_desc = "日期：{} 星期{}".format(item['date'], week_format[int(item['dayOfWeek'])])
            day_desc = "白天天气：{}, 白天温度：{}, 白天风向：{} , 白天风力：{}".format(item['dayWeather'], item['dayTemp'], item['dayWindDirection'], item['dayWindPower'])
            night_desc = "晚上天气：{}, 晚上温度：{}, 晚上风向：{} , 晚上风力：{}".format(item['nightWeather'], item['nightTemp'],
                                                               item['nightWindDirection'], item['nightWindPower'])
            content = content + """
### {}  
{}  
{}""".format(title_desc, day_desc, night_desc)
        ft_send(address + " 天气预报", content)


def sleep_notice():
    now = datetime.datetime.now()
    if now.strftime('%H') == '23' or debug:
        print('正在推送晚上睡觉提醒...')
        ft_send('同学，该睡觉了哦~', '早睡早起，身体倍棒！')


def ft_send(title, content):
    requests.get('http://sc.ftqq.com/SCU46796T4671f0d85ebce91e2c0ec5ee6b5c022e5c91ecec48d87.send?text=' + quote(title) + '&desp=' + quote(content))


if __name__ == "__main__":
    debug = False
    daily_greetings()
    sleep_notice()
    weather_notice()

