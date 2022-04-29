import time
import requests
import json
import datetime

from copy import deepcopy
from os.path import dirname, join, exists
import hoshino
from hoshino import R, Service, priv
from hoshino.util import FreqLimiter, DailyNumberLimiter
from hoshino.typing import CQEvent, MessageSegment

sv = Service('when2holiday')

today = time.time()

curpath = dirname(__file__)
data = join(curpath, 'data.json')
config =join(curpath,'config.json')
if exists(data):
    with open(data,'r', encoding='UTF-8') as fp:
        root = json.load(fp)
if exists(config):
    with open(config,'r',encoding='UTF-8') as fp:
        text = json.load(fp)
        
text1 = text['text']['text1']
holiday = root['holiday']
holiday_cache = {}
holiday_cache = deepcopy(holiday)

holiday_name1 = ['元旦','除夕','清明节','劳动节','端午节','中秋节','国庆节']
holiday_name2 = ['元旦','除夕','清明','五一','端午','中秋','国庆']

def get_message():
    holiday_check = [0,0,0,0,0,0,0]
    msg,msg_am,msg_pm = '','',''
    today = time.time()
    for data in holiday_cache:
        info = holiday_cache[data]
        timeArray = time.strptime(info['date'], "%Y-%m-%d")
        timeStamp = int(time.mktime(timeArray))
        for i in range(len(holiday_check)):
            if info['name'] == str(holiday_name1[i]) and holiday_check[i] == 0 and info['holiday'] == True and today < timeStamp:
                time_int = int((timeStamp - today)/86400) + 1
                msg_am = msg_am + f'距离【{holiday_name2[i]}】还有：{time_int}天\n'
                msg_pm = msg_pm + f'距离【{holiday_name2[i]}】还有：{time_int - 1}天\n'
                holiday_check[i] = 1
    d1 = datetime.datetime.now()
    to_weekend = 6 - datetime.datetime.now().isoweekday()
    msg_am = f'【摸鱼办】提醒您：{d1.month}月{d1.day}日上午好，'+ text1 + '\n' + f'距离【周末】还有：{to_weekend}天\n'+ msg_am
    msg_pm = f'【摸鱼办】提醒您：{d1.month}月{d1.day}日下午好，'+ text1 + '\n' + f'距离【周末】还有：{to_weekend-1}天\n'+ msg_pm
    msg_change_am = f'【摸鱼办】提醒您：{d1.month}月{d1.day}日下午好，'+ text1 + '\n' + f'今天是节假日调休\n'+ msg_am
    msg_change_pm = f'【摸鱼办】提醒您：{d1.month}月{d1.day}日下午好，'+ text1 + '\n' + f'今天是节假日调休\n'+ msg_pm
    url = f'https://timor.tech/api/holiday/info'
    print(url)
    r = requests.get(url)
    holiday = r.json()
    today_type = holiday['type']['type']
    print(today_type)
    if today_type == 0:                                     #工作日
        if datetime.datetime.now().hour < 12:
            msg=msg_am
        elif datetime.datetime.now().hour > 12:
            msg=msg_pm
    elif today_type == 3:                                   #调休
        if datetime.datetime.now().hour < 12:
            msg=msg_change_am
        elif datetime.datetime.now().hour > 12:
            msg=msg_change_pm
    return msg

@sv.on_fullmatch("测试假期推送")
async def send_holiday_message(bot, ev: CQEvent):
    try:
        msg = get_message()
        if msg != '':
            await bot.send(ev, str(msg))
    except Exception as e:
        print(e)
        await bot.send(ev, 'wuwuwu~~')



@sv.scheduled_job('cron',hour='9')
async def auto_send_holiday_message():
    #这边为定时发送消息
    #await bot.send(ev, "测试")
    msg = get_message()
    await sv.broadcast(msg, 'auto_send_holiday_message', 2)

@sv.scheduled_job('cron',hour='15')
async def auto_send_holiday_message():
    #这边为定时发送消息
    #await bot.send(ev, "测试")
    msg = get_message()
    await sv.broadcast(msg, 'auto_send_holiday_message',  2)
    
#@sv.on_fullmatch("123")   
#async def auto_send_holiday_message(bot, ev: CQEvent):
#    #这边类似广播操作，设置口令就能全群广播
#    await sv.broadcast("msg", 'auto_send_holiday_message', 0.2)
    

@sv.on_fullmatch("剩余假期")
async def year_holiday(bot, ev: CQEvent):
    false_holiday = 0
    holiday = 0
    msg = '今年剩余的假期有:\n'
    for data in holiday_cache:
        info = holiday_cache[data]
        timeArray = time.strptime(info['date'], "%Y-%m-%d")
        timeStamp = time.mktime(timeArray)
        if info['holiday'] == True and today < timeStamp:
            day = datetime.datetime.strptime(info['date'], "%Y-%m-%d").weekday()
            if day == 5 or day == 6:
                false_holiday = false_holiday + 1
            time_int = int((timeStamp - today)/86400)+ 1
            name = info['name']
            date = info['date']
            msg = msg + f'{date}{name},还有{time_int}天' + '\n'
            holiday = holiday +1
        elif info['holiday'] == False and today < timeStamp:
            false_holiday = false_holiday + 1
    real_holiday = holiday - false_holiday
    msg = msg + f'共{holiday}天\n减去调休与周末后剩余假期为{real_holiday}天'
    await bot.send(ev, msg)


#每天四点更新假期数据
@sv.scheduled_job('cron',hour='4')
async def today_holiday():
    url = 'http://timor.tech/api/holiday/year'
    r = requests.get(url)
    holiday = r.json()
    with open(data,'w', encoding='UTF-8') as f:
        json.dump(holiday, f)


