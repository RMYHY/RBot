from nonebot import on_command
from hoshino import Service, priv
from hoshino.typing import CQEvent

sv = Service('botlog', manage_priv=priv.SUPERUSER, visible=False, enable_on_default=True)

LOG = '''
2021.7.20 bot更新日志
如有建议请使用【来杯咖啡】
- 请珍惜bot尚存群内的时光 -
'''.strip()

@sv.on_fullmatch(('botlog', '更新日志'))
async def update_log(bot, ev):
    await bot.send(ev, f"{LOG}")
