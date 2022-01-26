import hoshino
from hoshino import Service, priv
from hoshino.typing import CQEvent

helpText = '请输入：一穿二 剩余秒数 BOSS血量 目标补偿（非必需）\n如：“一穿二 34 2000”或“一穿二 34 2000 56”'
sv = Service('一穿二', manage_priv=priv.SUPERUSER, help_=helpText)

def calc(x:float, y:float, *args:float) -> float:
    '''
    PCR补偿进位采用进一法
    补偿时间 = 固定补偿（国服目前为20s）+（90-（BOSS当前血量/实际造成伤害（最高为当前血量））*造成伤害的时间）
    '''
    if len(args) == 0:
        return float((y/(90-x))*(20+x+1))
    else:
        return float((y/(90-x))*(110-args[0]+1))


@sv.on_prefix('一穿二')
async def feedback(bot, ev: CQEvent):
    cmd = ev.raw_message
    content = cmd.split()
    lenC = len(content)
    if lenC != 4 and lenC != 3 and lenC != 1:
        await bot.send(ev, helpText + '\n错误0')
        return
    elif lenC == 1:
        await bot.send(ev, helpText)
        return
    try:
        c1 = float(content[1])
        c2 = float(content[2])
    except:
        await bot.send(ev, helpText + '\n错误1')
        return
    if c1 <= 0 or c2 <= 0 or c1 >= 90:
        await bot.send(ev, '输入数字错误。')
        return
    elif c1 >= 35:
        await bot.send(ev, '无需填补即可一穿二。')
        return
    if lenC == 3:
        result = calc(c1, c2)
        needs = c2 - result
    elif lenC == 4:
        try:
            c3 = float(content[3])
        except:
            await bot.send(ev, helpText + '\n错误2')
            return
        if not (c3 >= (c1+20) and c3 <= 90):
            await bot.send(ev, '目标补偿时间错误，必须不小于剩余时间+20s且不大于90s。')
            return
        result = calc(c1, c2, c3)
        needs = c2 - result
    reply = '若要按需求完成一穿二，应至少填{:.2f}伤害，使当前BOSS血量降至{:.2f}以下。'.format(needs, result)
    await bot.send(ev, reply)
