import os
from collections import defaultdict
import random
from hoshino import Service, R
from hoshino.typing import *
from hoshino.util import DailyNumberLimiter, pic2b64, concat_pic, silence
from hoshino import util
from hoshino.modules.priconne import chara
try:
    import ujson as json
except:
    import json

sv = Service('pcr-horse', enable_on_default=True, visible=True)

_pool_config_file = os.path.expanduser('~/.hoshino/group_pool_config.json')
_group_pool = {}
POOL = ('MIX', 'JP', 'TW', 'BL')
DEFAULT_POOL = POOL[0]

try:
    with open(_pool_config_file, encoding='utf8') as f:
        _group_pool = json.load(f)
except FileNotFoundError as e:
    sv.logger.warning('group_pool_config.json not found, will create when needed.')
_group_pool = defaultdict(lambda: DEFAULT_POOL, _group_pool)

lmt = DailyNumberLimiter(5)


special_object = [
    '๐',  '๐ง', '๐ฟ', '๐'
]


numb = ['1๏ธโฃ', '2๏ธโฃ', '3๏ธโฃ', '4๏ธโฃ']


class Palyer(object):

    def __init__(self, pool_name:str = "MIX"):
        super().__init__()
        self.load_chara(pool_name)

    def load_chara(self, pool_name:str):
        config = util.load_config(__file__)
        pool = config[pool_name]
        self.player = pool["player"]
        self.number = pool["number"]

    def get_chara(self):
        result = []
        c = chara.fromname(random.choice(self.player), 3)
        result.append(c)
        while len(result) != 4:
            c = chara.fromname(random.choice(self.player), 3)
            result_name = [f'{i.name}' for i in result]
            if c.name not in result_name:
                result.append(c)
        return result

    def get_num(self):
        result = []
        for _ in range(4):
            c = chara.fromname(self.number[_], 3)
            result.append(c)
        return result


g_result = []

g_uid = 0


def save_player(result_name):
    if result_name != []:
        global g_result
        g_result = [f'{c}' for c in result_name]
    else:
        g_result = []
        return


#็ๆๆจกๆ่ต้ๆฐ็ป(1โๆ?ๅถไป็ฉๅ๏ผ2โๅ?้ๅ๏ผ4โๅผน็ฐง่ทณๆฟ๏ผ0โไผ?้้ญๆณ้ต๏ผ-1โๆฐดๆดผ/็ณๅ/้ญ็ฉ)
def genl(a):
    px = []
    s = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, -1, -1, -1, -1, -1, -1, 4, 4, 0]
    for _ in range(a):
        random.shuffle(s)
        i = random.randint(0, len(s) - 1)
        x = s[i]
        px.append(x)
        if x == 0:
            for _i in range(_ + 1, a - 2):
                x = 1
                px.append(x)
            x = 0
            px.append(x)
            x = s[random.randint(0, len(s) - 1)]
            px.append(x)
            return px
    return px

#่ฝฌๆขๆฐ็ปไธบ็ฌฆๅท&emoji
def gen_w(l, i:int):
    m = f'{numb[i-1]}'
    for _ in l:
        if _ == 1:
            m += f'โฐ'
        if _ == 2:
            m += f'โฉ'
        if _ == 4:
            m += f'๐ท'
        if _ == -1:
            m += f'{random.choice(special_object)}'
        if _ == 0:
            m += f'โก'
    return m



def step(y, z:int):
    x = 0
    if y[z] != 0:
        x = y[z]
        return x
    if y[z] == 0:
        x = 13 - z
        return x


#้ป่พๆๅพไผๅ๏ผ้็ผ็จไธไธๆๅคช่ไบQAQ
async def compe(bot, ev: CQEvent, p:str):
    global g_result
    r = 15
    result = []
    msg = f'========================\n'
    pa = genl(r)
    pb = genl(r)
    pc = genl(r)
    pd = genl(r)
    pri = []
    r_pri = []
    stone = [500, 400, 300, 250]
    a = b = c = d = 0
    await bot.send(ev, f'{gen_w(pa, 1)}\n{gen_w(pb, 2)}\n{gen_w(pc, 3)}\n{gen_w(pd, 4)}')
    for _ in range(r):
        a += step(pa, _)
        b += step(pb, _)
        c += step(pc, _)
        d += step(pd, _)
        if a >= r:
            pri.append(g_result[0])
        if b >= r:
            pri.append(g_result[1])
        if c >= r:
            pri.append(g_result[2])
        if d >= r:
            pri.append(g_result[3])
    pri_r = [a, b, c, d]
    pri_r = sorted(pri_r, reverse=True)
    for _ in pri_r:
        if a == _:
            pri.append(g_result[0])
        if b == _:
            pri.append(g_result[1])
        if c == _:
            pri.append(g_result[2])
        if d == _:
            pri.append(g_result[3])
    for k in pri:
        if k not in r_pri:
            r_pri.append(k)
    for i in range(0, 4):
        msg += f'็ฌฌ{i+1}ไฝ๏ผ{r_pri[i]}\n'
    for j in range(4):
        if p == r_pri[j]:
            msg += f'ๆญๅ่ทๅพ็ฌฌ{j+1}ไฝๅฅๅฑ๏ผๅฎ็ณร{stone[j]}\n========================'
            silence_time = (3 - j) * 30
    await bot.send(ev, msg)
    await silence(ev, silence_time)
    save_player(result)




async def select_player(bot, ev: CQEvent):
    global g_result, g_uid
    pkey = ev.message.extract_plain_text().strip()
    id_ = chara.name2id(pkey)
    p = chara.fromid(id_)
    if p.name not in g_result:
        await bot.finish(ev, f'ๆ้่ง่ฒๆชๅจๅ่ต่ง่ฒไธญ')
    await bot.send(ev, f'ๅทฒ้ๆฉ{p.name},ๆฏ่ตๅผๅง', at_sender=True)
    await compe(bot, ev, p.name)
    g_uid = 0



@sv.on_fullmatch(('่ต้ฉฌๅผๅง'), only_to_me=True)
async def pcr_comp(bot, ev: CQEvent):
    global g_result, g_uid
    uid = ev.user_id
    if not lmt.check(uid):
        await bot.send(ev, 'ไปๅคฉๅทฒ็ป่ต่ฟ5ๆฌกๅ', at_sender=True)
        return
    if g_result != []:
        await bot.send(ev, 'ไธไธๅบๆฏ่ตๅฐๆช็ปๆ๏ผ่ฏท็ญๅพ', at_sender=True)
        return
    lmt.increase(uid)
    await bot.send(ev, f'็ฌฌโๅฑๅฐๅพท็ดขๅฐๆฏๆฏ่ตๅผๅง๏ผ', at_sender=True)
    gid = str(ev.group_id)
    palyer = Palyer(_group_pool[gid])
    result = palyer.get_chara()
    result_number = palyer.get_num()
    res2 = chara.gen_team_pic(result, star_slot_verbose=False)
    res1 = chara.gen_team_pic(result_number, star_slot_verbose=False)
    res = concat_pic([res1, res2])
    res = pic2b64(res)
    res = MessageSegment.image(res)
    result_name = [f'{c.name}' for c in result]
    res_name = ' '.join(result_name)
    if sv.bot.config.USE_CQPRO:
        await bot.send(ev, f'ๆฏ่ต้ๆ๏ผ\n{res}\n{res_name}\nโปๅ้โ้ไธญ+่ง่ฒๅ็งฐโๅผๅงๆฏ่ต', at_sender=False)
    else:
        await bot.send(ev, f'error:CQpro is required')
    save_player(result_name)
    g_uid = uid

@sv.on_prefix('้ไธญ')
async def _select_(bot, ev):
    global g_uid, g_result
    uid = ev.user_id
    if uid != g_uid and g_result != []:
        await bot.finish(ev, f'ไป้ๆฏ่ตๅ่ตทไบบ่ฟ่ก้ๆฉ~')
    if uid != g_uid and g_result == []:
        await bot.finish(ev, f'ไธไธๅบๆฏ่ตๅทฒ็ป็ปๆ๏ผๆจๅฏไปฅ็จโๆฉๅ็ฑ่ต้ฉฌๅผๅงโๅ่ตทๆฐ็ๆฏ่ต', at_sender=True)
    if uid == g_uid:
        await select_player(bot, ev)
    else:
        await bot.finish(ev, f'ๅบ็ฐ้่ฏฏ๏ผ่ฏท่็ณป็ปดๆค็ปๅคๅคๅค')


