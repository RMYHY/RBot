# Partially refer to the code of priconne games in HoshinoBot by @Ice-Cirno
# Under GPL-3.0 License

import asyncio
import os
import random
import aiohttp
import requests
import datetime
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup

import hoshino
from hoshino import Service, priv, R, log
from hoshino.util import DailyNumberLimiter
from hoshino.modules.priconne import chara
from hoshino.modules.priconne.pcr_duel import ScoreCounter2
from hoshino.typing import MessageSegment, CQEvent
from . import GameMaster
from nonebot import scheduler


sv_help = '''
- [猜现实] 猜猜随机的角色现实图片是哪位角色
'''.strip()

sv = Service(name = '猜现实',  use_priv = priv.NORMAL,   manage_priv = priv.ADMIN, visible = True,enable_on_default = True, bundle = '娱乐',help_ = sv_help)

@sv.on_fullmatch(["帮助猜现实"])
async def bangzhu(bot, ev):
    await bot.send(ev, sv_help, at_sender=True)

PRICE = 150 #获胜所得的金币
MAX_NUM = 6 #每日获得的金币次数
DOWNLOAD_THRESHOLD = 142
MULTIPLE_VOICE_ESTERTION_ID_LIST = ['0044']
ONE_TURN_TIME = 15
HOSHINO_RES_PATH = os.path.expanduser(hoshino.config.RES_DIR)
DIR_PATH = os.path.join(HOSHINO_RES_PATH, 'img/priconne/unit/actual')
DB_PATH = os.path.expanduser("~/.hoshino/pcr_actual_guess.db")

gm = GameMaster(DB_PATH)
lm = DailyNumberLimiter(MAX_NUM)

def get_estertion_id_list():
    url = 'https://redive.estertion.win/card/actual_profile'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    l = []
    for a in soup.find_all('a'):
        s = a['href']
        l.append(s)
    return l

logger = log.new_logger('actual_guess', hoshino.config.DEBUG)
async def download(url, save_path):
    logger.info(f'Downloading chara actual phtot from {url}')
    try:
        rsp = requests.get(url, stream=True, timeout=30)
    except Exception as e:
        logger.error(f'Failed to download {url}. {type(e)}')
        logger.exception(e)
        return False
    if 200 == rsp.status_code:
        img = Image.open(BytesIO(rsp.content))
        img.save(save_path)
        logger.info(f'Saved to {save_path}')
        return True
    else:
        logger.error(f'Failed to download {url}. HTTP {rsp.status_code}')
        return False


async def download_actual_photo(bot, ev: CQEvent):
    if not os.path.exists(DIR_PATH):
        os.makedirs(DIR_PATH)
    file_name_list = os.listdir(DIR_PATH)
    file_name_list_no_suffix = [file.rsplit('.', 1)[0] for file in file_name_list]
    if len(file_name_list) < DOWNLOAD_THRESHOLD:
        count = 0
        await bot.send(ev, '正在下载角色现实图片资源，请耐心等待')
        estertion_id_list = get_estertion_id_list()
        for eid in estertion_id_list:
            url = f'https://redive.estertion.win/card/actual_profile/{eid}'
            file_name = url.split('/')[-1]
            if file_name.rsplit('.', 1)[0] not in file_name_list_no_suffix:
                file_path = os.path.join(DIR_PATH, file_name.split('.')[0] + '.png')
                if not await download(url, file_path):
                    pass
                else:
                    count = count + 1
        await bot.send(ev, f'下载完毕，此次下载角色现实图片{count}个，目前共{len(os.listdir(DIR_PATH))}个')


@sv.on_fullmatch(("猜现实排行", "猜现实排行榜", "猜现实群排行"))
async def acutal_guess_group_ranking(bot, ev: CQEvent):
    ranking = gm.db.get_ranking(ev.group_id)
    msg = ["【猜现实小游戏排行榜】"]
    for i, item in enumerate(ranking):
        uid, count = item
        m = await bot.get_group_member_info(self_id=ev.self_id, group_id=ev.group_id, user_id=uid)
        name = m["card"] or m["nickname"] or str(uid)
        msg.append(f"第{i + 1}名: {name}, 猜对{count}次")
    await bot.send(ev, "\n".join(msg))


@sv.on_fullmatch('猜现实')
async def actual_guess(bot, ev: CQEvent):
    if gm.is_playing(ev.group_id):
        await bot.finish(ev, "游戏仍在进行中…")
    if not os.path.exists(DIR_PATH) or len(os.listdir(DIR_PATH)) < DOWNLOAD_THRESHOLD:
        await download_actual_photo(bot, ev)
        return
    # with gm.start_game(ev.group_id) as game:
    game = gm.start_game(ev.group_id)
    file_list = os.listdir(DIR_PATH)
    chosen_chara = random.choice(file_list)
    await bot.send(ev, f'猜猜这张图片是哪个角色? ({ONE_TURN_TIME}s后公布答案)')
    await bot.send(ev, R.img(f'priconne/unit/actual/{chosen_chara}').cqcode)
    game.answer = int(chosen_chara[0:4])
    game.set_schedule(scheduler.add_job(check, 'date', args=(bot, ev,), next_run_time=datetime.datetime.now() + datetime.timedelta(seconds = ONE_TURN_TIME)))
    #     await asyncio.sleep(ONE_TURN_TIME)
    #     # 结算
    #     if game.winner:
    #         return
    #     c = chara.fromid(game.answer)
    # await bot.send(ev, f"正确答案是: {c.name} {c.icon.cqcode}\n很遗憾，没有人答对~")

async def check(bot, ev):
    game = gm.get_game(ev.group_id)
    if game.winner:
        return
    c = chara.fromid(game.answer)
    gm.exit_game(ev.group_id)
    await bot.send(ev, f"正确答案是: {c.name} {c.icon.cqcode}\n很遗憾，没有人答对~")


@sv.on_message()
async def on_input_chara_name(bot, ev: CQEvent):
    game = gm.get_game(ev.group_id)
    if not game or game.winner:
        return
    c = chara.fromname(ev.message.extract_plain_text())
    if c.id != chara.UNKNOWN and c.id == game.answer:
        game.winner = ev.user_id
        n = game.record()
        uid = ev.user_id
        gid = ev.group_id
        msg = f"正确答案是: {c.name}{c.icon.cqcode}\n{MessageSegment.at(ev.user_id)}猜对了，真厉害！TA已经猜对{n}次了~\n"
        if lm.check((gid, uid)):
            msg += f'TA获得了{PRICE}金币！'
            lm.increase((gid, uid))
            score_counter = ScoreCounter2()
            score_counter._add_score(gid, uid, PRICE)
        else:
            msg += f'由于本游戏每日可获得最多{MAX_NUM}次金币，所以本次游戏TA将不再获得。'
        game.remove_schedule()
        gm.exit_game(ev.group_id)
        await bot.send(ev, msg)
