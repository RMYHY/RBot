Skip to content
Search or jump to…
Pull requests
Issues
Marketplace
Explore
 
@RMYHY 
qiuyue0
/
pcr_timecalc
Public
forked from madoka315/pcr_timecalc
0
12
Code
Issues
2
Pull requests
Actions
Projects
Wiki
Security
Insights
pcr_timecalc/pcrtimecalc.py /
@qiuyue0
qiuyue0 去掉了不必要的说明
Latest commit c00dc84 8 days ago
 History
 2 contributors
@qiuyue0@madoka315
55 lines (53 sloc)  2.16 KB
   
import hoshino
import math
from hoshino import Service, priv
from hoshino.typing import CQEvent

sv = Service('合刀', manage_priv=priv.SUPERUSER, help_='请输入：合刀 刀A伤害 刀B伤害 剩余血量 [击杀刀剩余时间]\n如：合刀 500 600 700')
class time_calc():
    def __init__(self,dmg1:float,dmg2:float,rest:float,left_time:int):
        self.dmg_A = min(rest,dmg1)
        self.dmg_B = min(rest,dmg2)
        self.rest=rest
        self.left_time=left_time
    def _range(self,num):
        return round(max(min(num,90.0),21.0),2)
    def A_first(self)->str:
        ret = self._range(110-(self.rest-self.dmg_A)/self.dmg_B*(90-self.left_time))
        return str(ret)
    def B_first(self)->str:
        ret = self._range(110-(self.rest-self.dmg_B)/self.dmg_A*(90-self.left_time))
        return str(ret)
@sv.on_prefix('合刀')
async def feedback(bot, ev: CQEvent):
    cmd = ev.raw_message
    content=cmd.split()
    if(len(content) not in (4,5)):
        reply="请输入：合刀 刀A伤害 刀B伤害 剩余血量 [击杀刀剩余时间]\n如：合刀 500 600 700"
        await bot.send(ev, reply)
        return
    try:
        left_time = float(content[4])
    except:
        left_time = 0
    d1=float(content[1])
    d2=float(content[2])
    rest=float(content[3])
    if(d1+d2<rest):
        reply="醒醒！这两刀是打不死boss的\n"
        await bot.send(ev, reply)
        return
    result = time_calc(d1,d2,rest,left_time)
    
    reply=f"刀A伤害：{d1} 刀B伤害：{d2} BOSS血量：{rest} "
    reply+=f"击杀刀剩余时间：{left_time}秒\n" if d1>=rest or d2>=rest else "\n"
    if(d1>=rest or d2>=rest):
        if(d2>=rest):
            reply=reply+"刀A先出，另一刀可获得 "+result.A_first()+" 秒补偿刀"
            await bot.send(ev, reply)
            return
        elif(d1>=rest):
            reply=reply+"刀B先出，另一刀可获得 "+result.B_first()+" 秒补偿刀"
            await bot.send(ev, reply)
            return
    reply=reply+"刀A先出，另一刀可获得 "+result.A_first()+" 秒补偿刀\n"
    reply=reply+"刀B先出，另一刀可获得 "+result.B_first()+" 秒补偿刀"
    await bot.send(ev, reply)
© 2021 GitHub, Inc.
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
