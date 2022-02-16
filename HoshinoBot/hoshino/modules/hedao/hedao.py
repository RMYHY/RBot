import math
from hoshino import Service
from hoshino.typing import CQEvent, MessageSegment

sv = Service('合刀', enable_on_default=True, help_='''尾刀计算器''')

#110 - (90-t)(boss/x) = 89

delta = 0.0000001

helpMsg = "请输入boss剩余血量和两刀伤害（可只输一刀或不输入）\n或：boss血量、造成伤害（缺省为boss血量）、打死时间、期望时间（可无）\n例：cal 700w 400 5000000 / cal 2000 34s 56s"


@sv.on_prefix(['尾刀计算', 'cal', '合刀'])
async def cal(bot, ev: CQEvent):
    msg = ev.message.extract_plain_text().strip()
    msg = msg.replace('w', '0000').replace('W', '0000').replace('万', '0000').split(' ')
    msg = list(filter(lambda L: L != '', msg))
    dam = []
    tim = []
    for x in msg:
        try:
            if x[-1] == 's':
                x = x[:-1]
                x = int(x)
                if x <= 0 or x >= 90:
                    await bot.finish(ev, f"时间错误：{x}")
                tim.append(x)
            else:
                x = float(eval(x))
                if x <= 0:
                    await bot.finish(ev, f"伤害为负：{x}")
                    return
                if x < 50000:
                    x *= 10000
                    f = 0
                x = int(x)
                dam.append(x)
        except:
            await bot.finish(ev, helpMsg)
            return
    print(dam, tim)
    eigen = str(len(dam)) + str(len(tim))

    if eigen == "10":  # cal 1500
        boss = dam[0]
        outp = f"HP={boss}\n"
        x = int(boss * 90 / 111)
        #x = boss / (n-1 + 21/90) n刀满补所需伤害
        outp += "刀数 / 满补所需伤害\n"
        for i in range(1, 5):
            outp += f"{i}刀 \t {int(math.ceil(delta + boss/(i-1+21/90)))}\n"
        await bot.finish(ev, f"{outp}")
    elif eigen == "01":  # cal 50s
        boss = tim[0]
        y = min(boss + 20, 90)
        await bot.finish(ev, f"补偿{y}秒")
    elif eigen == "20":  # cal 700 300 / cal 300 700
        boss = dam[0]
        x = dam[1]
        outp = f"HP={boss}\ndamage={x}\n"
        if x >= boss:
            y = min(90, int(math.ceil(110 - 90 * boss / x)))
            outp += f"补偿{y}秒"
            if y < 90:
                z = int(math.ceil(delta + boss - 21 / 90 * x))
                outp += f"\n垫入{z}伤害可满补"
            await bot.finish(ev, outp)
        y = int(math.ceil(delta + 90 / 21 * (boss - x)))
        yy = int(math.ceil(delta + boss - 21 / 90 * x))
        if yy < y:
            outp += f"另一刀伤害达到{yy}(先出)/{y}(后出)即可满补。"
        else:
            outp += f"另一刀伤害达到{y}(后出)即可满补。"
        await bot.finish(ev, outp)
    elif eigen == "30":  # cal 400 500 700 / cal 700 100 200
        boss = max(dam[0], dam[1], dam[2])
        y = min(dam[0], dam[1], dam[2])
        x = dam[0] + dam[1] + dam[2] - boss - y
        outp = f"HP={boss}\ndamage1={x}\ndamage2={y}\n"
        if x + y < boss:
            outp += f"剩余血量{int(boss - x - y)}"
        else:
            ti1 = min(90, int(math.ceil(110 - 90 * (boss - x) / y)))
            ti2 = min(90, int(math.ceil(110 - 90 * (boss - y) / x)))
            outp += f"补偿{ti1}秒/{ti2}秒"
        await bot.finish(ev, outp)
    elif eigen == "21":  # 1800 2000 34s
        boss = min(dam[0], dam[1])
        x = max(dam[0], dam[1])
        t = tim[0]
        outp = f"HP={boss}\ndamage={x}余{t}s\n"
        remain = int(math.ceil(110 - (90 - t) * (boss / x)))
        outp += f"返还{remain}s"
        await bot.finish(ev, outp)
    elif eigen in ["12", "22", "11"]:  # 700 30s 61s
        boss = dam[0]
        x = boss
        if eigen == "22":  # 1800 2000 34s 58s
            boss = min(dam[0], dam[1])
            x = max(dam[0], dam[1])
        t = tim[0]
        tt = 91 - t
        if eigen == 12:
            t = min(tim[0], tim[1])
            tt = max(tim[0], tim[1])
        outp = f"HP={boss}\ndamage={x}余{t}s\n期望获得{tt}s\n"
        remain = min(int(math.ceil(110 - (90 - t) * (boss / x))), 90)
        y = int(math.ceil(delta + boss - x * (111 - tt) / (90 - t)))
        if y > 0:
            outp += f"还需垫入{y}伤害"
        else:
            outp += f"已满足要求（余{remain}s）"
        await bot.finish(ev, outp)
    else:
        await bot.finish(ev, helpMsg)
