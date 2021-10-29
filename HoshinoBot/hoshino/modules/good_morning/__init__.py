from hoshino import Service, priv
import hoshino
import os
from .get_morning import *
from .get_night import *

sv = Service('good_morning', bundle='早安晚安')

sv_help = '''[早安晚安初始化] 初始化，限超级管理员
[早安] 早安喵
[晚安] 晚安喵
[我的作息] 看看自己的作息
[群友作息] 看看今天几个人睡觉或起床了'''.strip()

#帮助界面
@sv.on_fullmatch('早安晚安帮助')
async def help(bot, ev):
    await bot.send(ev, sv_help)

@sv.on_fullmatch('早安晚安初始化')
async def create_json(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        msg = '很抱歉您没有权限进行此操作，该操作仅限维护组'
        await bot.send(ev, msg)
        return
    try:
        group_list = await bot.get_group_list()
        for each_g in group_list:
            group_id = each_g['group_id']
            _current_dir = os.path.join(os.path.dirname(__file__), f'data\{group_id}.json')
            if not os.path.exists(_current_dir):
                data = {
                    "today_count": {
                        "morning": 0,
                        "night": 0
                    }
                }
                with open(_current_dir, "w", encoding="UTF-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                msg = '早安晚安初始化成功！'
            else:
                msg = '配置文件已存在请勿重复生成！'
    except:
        msg = '早安晚安初始化失败！'
    await bot.send(ev, msg)

@sv.on_fullmatch('早安')
async def good_morning(bot, ev):
    user_id = ev.user_id
    group_id = ev.group_id
    mem_info = await bot.get_group_member_info(group_id = group_id, user_id = user_id)
    sex = mem_info['sex']
    if sex == 'male':
        sex_str = '少年'
    elif sex == 'female':
        sex_str = '少女'
    else:
        sex_str = '群友'
    msg = get_morning_msg(group_id, user_id, sex_str)
    await bot.send(ev, msg)

@sv.on_fullmatch('晚安')
async def good_night(bot, ev):
    user_id = ev.user_id
    group_id = ev.group_id
    mem_info = await bot.get_group_member_info(group_id = group_id, user_id = user_id)
    sex = mem_info['sex']
    if sex == 'male':
        sex_str = '少年'
    elif sex == 'female':
        sex_str = '少女'
    else:
        sex_str = '群友'
    msg = get_night_msg(group_id, user_id, sex_str)
    await bot.send(ev, msg)

# 23:59清除一天的早安晚安计数
@sv.scheduled_job('cron', hour='23', minute='59')
async def reset_data():
    bot = hoshino.get_bot()
    group_list = await bot.get_group_list()
    for each_g in group_list:
        group_id = each_g['group_id']
        current_dir = os.path.join(os.path.dirname(__file__), f'data\{group_id}.json')
        file = open(current_dir, 'r', encoding = 'UTF-8')
        data = json.load(file)
        data['today_count']['morning'] = 0
        data['today_count']['night'] = 0
        with open(current_dir, "w", encoding="UTF-8") as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))

@sv.on_fullmatch('我的作息')
async def my_status(bot, ev):
    user_id = ev.user_id
    group_id = ev.group_id
    current_dir = os.path.join(os.path.dirname(__file__), f'data\{group_id}.json')
    file = open(current_dir, 'r', encoding = 'UTF-8')
    data = json.load(file)
    if str(user_id) in list(data.keys()):
        get_up_time = data[str(user_id)]['get_up_time']
        sleep_time = data[str(user_id)]['sleep_time']
        morning_count = data[str(user_id)]['morning_count']
        night_count = data[str(user_id)]['night_count']
        msg = f'[CQ:at,qq={user_id}]您的作息数据如下：'
        msg = msg + f'\n最近一次起床时间为{get_up_time}'
        msg = msg + f'\n最近一次睡觉时间为{sleep_time}'
        msg = msg + f'\n一共起床了{morning_count}次'
        msg = msg + f'\n一共睡觉了{night_count}次'
    else:
        msg = '您还没有睡觉起床过呢！暂无数据'
    await bot.send(ev, msg)

@sv.on_fullmatch('群友作息')
async def group_status(bot, ev):
    group_id = ev.group_id
    current_dir = os.path.join(os.path.dirname(__file__), f'data\{group_id}.json')
    file = open(current_dir, 'r', encoding = 'UTF-8')
    data = json.load(file)
    moring_count = data['today_count']['morning']
    night_count = data['today_count']['night']
    msg = f'今天已经有{moring_count}位群友起床了，{night_count}群友睡觉了'
    await bot.send(ev, msg)