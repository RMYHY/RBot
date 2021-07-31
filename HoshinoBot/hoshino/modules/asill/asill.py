import requests, random, os, json
from hoshino import Service, R
from hoshino.typing import CQEvent
from hoshino.util import FreqLimiter
import hoshino

sv = Service('asill', enable_on_default=True, visible=True,help_='''
[发病 对象] 对发病对象发病
[小作文] 随机发送一篇发病小作文
[病情加重 对象/小作文] 将一篇发病小作文添加到数据库中（必须带“/”）
'''.strip())

def get_data():
    _path = os.path.join(os.path.dirname(__file__), 'data.json')
    if os.path.exists(_path):
        with open(_path,"r",encoding='utf-8') as df:
            try:
                words = json.load(df)
            except Exception as e:
                hoshino.logger.error(f'读取发病小作文时发生错误{type(e)}')
                return None
    else:
        hoshino.logger.error(f'目录下未找到发病小作文')
    return random.choice(words)


@sv.on_keyword('小作文')
async def xzw(bot,ev:CQEvent):
    gid = ev.group_id
    illness = get_data()
    await bot.send(ev, illness["text"])

@sv.on_prefix('发病')
async def fb(bot, ev: CQEvent):
    aim = str(ev.message).strip()
    if not aim:
        await bot.send(ev, "请发送[发病 对象]~", at_sender=True)
    else:
        illness = get_data()
        text = illness["text"]
        person = illness["person"]
        text = text.replace(person,aim)
        await bot.send(ev, text)

@sv.on_prefix('病情加重')
async def bqjz(bot, ev: CQEvent):
    kw = ev.message.extract_plain_text().strip()
    arr = kw.split('/')
    if not arr[0] or not arr[1] or len(arr) > 2:
        await bot.send(ev, "请发送[病情加重 对象/小作文]（必须带“/”）~", at_sender=True)
    else: 
        new_illness = {"person" : arr[0], "text" : arr[1]}
        _path = os.path.join(os.path.dirname(__file__), 'data.json')
        words = None
        if os.path.exists(_path):
            with open(_path,"r",encoding='utf8') as df:
                try:
                    words = json.load(df)
                except Exception as e:
                    hoshino.logger.error(f'读取发病小作文时发生错误{type(e)}')
                    return None
            words.append(new_illness)        
            with open(_path,"w",encoding='utf8') as df:        
                try:
                    json.dump(words,df,indent=4)
                    await bot.send(ev, "病情已添加", at_sender=True)
                except Exception as e:
                    hoshino.logger.error(f'添加发病小作文时发生错误{type(e)}')
                    return None
        else:
            hoshino.logger.error(f'目录下未找到发病小作文')
    
