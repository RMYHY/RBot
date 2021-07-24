from hoshino import R, Service, priv
from hoshino.typing import CQEvent

sv = Service('_help_', manage_priv=priv.SUPERUSER, visible=False)

HELP_MANUAL = '''
=====================
-    Bot使用说明    -
=====================
※可用呼唤bot名字来代替@bot，可供使用的呢称有：bot, hina, 氷川日菜
※[lssv]列出的功能群管理可控制开关
  [启用/禁用 service-name]
※具体的指令可以通过[service-name帮助/说明]查看
  例：[setu帮助]  #查看setu功能的详细说明
※使用本bot即默认您知晓bot提供的涩图等服务的风险。若因此导致封群bot概不负责
※本bot定期更新，可使用[更新日志]来查看更新内容
※详细功能说明：https://github.com/RMYHY/RBot/blob/main/HELP.md
※项目地址：https://github.com/RMYHY/RBot
---感谢您选择本bot！祝您使用愉快！---
'''.strip()

@sv.on_fullmatch(('使用指南', '使用说明', '使用帮助', '使用手册','高级使用技巧', '使用技巧', '高级技巧'))
async def main_help(bot, ev: CQEvent):
        await bot.send(ev, f"{HELP_MANUAL}")

COMMAND_MANUAL1 = '''
- Bot指令表 -
篇幅原因，每种功能只取一项指令，详细的指令请通过(服务名)[帮助/说明]查看
=====================
（1/2）
【授权帮助】   查看群bot授权情况
【开空调】    群内模拟中央空调
【来杯咖啡】    向bot主人发送反馈
【失信114514】  根据ID查找公会黑名单人员
【今日日程】    查看今天的pcr日程
【公会排名卢本伟】  查询公会名字包含卢本伟的公会排名
【.r 3d12】  掷3次12面骰子
【搜无损 恋爱循环】  搜索《恋爱循环》的无损歌曲
【爆裂魔法】    每天一发惠惠爆裂魔法！
【营销号 主体/事件/另一种说法】 营销文生成器
【更新日志】  查看bot当前更新日志
【切噜一下 我爱璃乃】   切噜～♪切蹦巴叮拉切噼蹦噜卟巴啰噜哔巴噼巴
【官漫132】  阅览132话官方四格漫画
【生成表情 小仓唯举报 不能ghs】   生成表情包
(@bot)【签到】    签到到
【挖矿 15001】  查询当前排名剩余矿存
====================
发送【帮助下一页】查看下页指令
*本指令表不含会战指令，查看会战指令表请发送【help】或【!help】*
'''.strip()

@sv.on_fullmatch(('指令表', '命令表', '指令集', '命令集', '帮助上一页'))
async def send_command1(bot, ev: CQEvent):
        await bot.send(ev, COMMAND_MANUAL1)

COMMAND_MANUAL2 = '''
- Bot指令表 -
篇幅原因，每种功能只取一项指令，详细的指令请通过(服务名)[帮助/说明]查看
=====================
（2/2）
【rank表】  查看rank推荐表
【谁是优衣】    角色别称查询
【精致睡眠】    bot禁言帮助睡觉觉
(@bot)【来发十连】    模拟十连抽奖
【猜角色】    猜一猜这个角色是谁？
【我问xxx你答yyy】  记录个人Q&A
【来点pcr表情包】   发送pcr公会表情包
【来点涩图】    注意身体
【网抑云】  随机网易云语录
【赛马开始】  简易模拟pcr赛马
【生成会战报告】  生成当期会战报告
【搜图+图】  根据图片搜画师和出处
【搜番+图】  根据截图搜番剧出处
【俄罗斯轮盘】  模拟俄罗斯轮盘
【抽签】     来一发vtb定制签
====================
*本指令表不含会战指令，查看会战指令表请发送【help】或【!help】*
'''.strip()

@sv.on_fullmatch(('帮助下一页', '指令下一页', '下一页'))
async def send_command2(bot, ev: CQEvent):
        await bot.send(ev, COMMAND_MANUAL2)
