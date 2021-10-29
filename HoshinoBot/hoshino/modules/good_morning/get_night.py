import os
import json
import datetime

# 重写构造json类
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)

# 判断晚安时间
def judge_sle_time(early_time_tmp, late_time_tmp, now_time):
    early_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + f' {early_time_tmp}:00:00', '%Y-%m-%d %H:%M:%S')
    late_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + f' {late_time_tmp}:00:00', '%Y-%m-%d %H:%M:%S')
    if now_time < early_time and now_time > late_time:
        return False
    return True

# 判断多次晚安
def judge_have_sle(data, user_id, now_time, interval):
    sleep_time = datetime.datetime.strptime(data[str(user_id)]['sleep_time'], '%Y-%m-%d %H:%M:%S')
    # 上次晚安时间和现在时间相差不超过f'{interval}'小时
    if sleep_time + datetime.timedelta(hours = int(interval)) > now_time:
        return True
    return False

# 判断超级睡眠
def judge_super_sleep(data, user_id, now_time, interval):
    get_up_time = datetime.datetime.strptime(data[str(user_id)]['get_up_time'], '%Y-%m-%d %H:%M:%S')
    # 上次起床时间和现在时间相差不超过f'{interval}'小时
    if get_up_time + datetime.timedelta(hours = int(interval)) > now_time:
        return True
    return False

# 进行晚安并更新数据
def night_and_update(_current_dir, data, user_id, now_time):
    # 若之前没有数据就直接创建一个
    if not str(user_id) in list(data.keys()):
        mem_data = {
            "morning_count": 0,
            "get_up_time": 0,
            "night_count": 1,
            "sleep_time": now_time
        }
        data.setdefault(str(user_id), mem_data)
    # 若有就更新数据
    else:
        data[str(user_id)]['sleep_time'] = now_time
        data[str(user_id)]['night_count'] = int(data[str(user_id)]['night_count']) + 1
    # 当上次起床时间不是初始值0,就计算清醒的时长
    in_day_tmp = 0
    if data[str(user_id)]['get_up_time'] != 0:
        get_up_time = datetime.datetime.strptime(data[str(user_id)]['get_up_time'], '%Y-%m-%d %H:%M:%S')
        in_day = now_time - get_up_time
        secs = in_day.total_seconds()
        day = secs // (3600 * 24)
        hour = (secs - day * 3600 * 24) // 3600
        minute = (secs - day * 3600 * 24 - hour * 3600) // 60
        second = secs - day * 3600 * 24 - hour * 3600 - minute * 60
        if day == 0:
            in_day_tmp = str(int(hour)) + '时' + str(int(minute)) + '分' + str(int(second)) + '秒'
    # 判断是今天第几个睡觉的
    data['today_count']['night'] = int(data['today_count']['night']) + 1
    with open(_current_dir, "w", encoding="UTF-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4, cls=DateEncoder))
    return data['today_count']['night'], in_day_tmp

# 返回晚安信息
def get_night_msg(group_id, user_id, sex_str):
    # 读取配置文件
    current_dir = os.path.join(os.path.dirname(__file__), 'config.json')
    file = open(current_dir, 'r', encoding = 'UTF-8')
    config = json.load(file)

    # 读取早安晚安数据
    _current_dir = os.path.join(os.path.dirname(__file__), f'data\{group_id}.json')
    file = open(_current_dir, 'r', encoding = 'UTF-8')
    data = json.load(file)

    # 若开启规定时间晚安，则判断该时间是否允许晚安
    now_time = datetime.datetime.now()
    if config['night']['sleep_intime']['enable']:
        early_time_tmp = config['night']['sleep_intime']['early_time']
        late_time_tmp = config['night']['sleep_intime']['late_time']
        if not judge_sle_time(early_time_tmp, late_time_tmp, now_time):
            msg = f'现在不能晚安哦，可以晚安的时间为{early_time_tmp}时到第二天早上{late_time_tmp}时'
            return msg

    # 当数据里有过这个人的信息就判断:
    if str(user_id) in list(data.keys()):
        # 若关闭连续多次晚安，则判断在设定时间内是否多次晚安
        if not config['night']['multi_sleep']['enable']:
            interval = config['night']['multi_sleep']['interval']
            if judge_have_sle(data, user_id, now_time, interval):
                msg = f'{interval}小时内你已经晚安过了哦'
                return msg
        # 若关闭超级睡眠，则判断不在睡觉的时长是否小于设定时长
        if not config['night']['super_sleep']['enable'] and data[str(user_id)]['get_up_time'] != 0:
            interval = config['night']['super_sleep']['interval']
            if judge_super_sleep(data, user_id, now_time, interval):
                msg = f'睡这么久还不够？现在不能晚安哦'
                return msg

    # 当数据里没有这个人或者前面条件均符合的时候，允许晚安
    num, in_day = night_and_update(_current_dir, data, user_id, now_time)
    if in_day == 0:
        msg = f'晚安成功！你是今天第{num}个睡觉的{sex_str}'
    else:
        msg = f'晚安成功！你今天的清醒时长为{in_day}。\n你是今天第{num}个睡觉的{sex_str}'
    return msg