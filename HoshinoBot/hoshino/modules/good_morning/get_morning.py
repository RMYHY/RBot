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

# 判断早安时间
def judge_mor_time(early_time_tmp, late_time_tmp, now_time):
    early_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + f' {early_time_tmp}:00:00', '%Y-%m-%d %H:%M:%S')
    late_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + f' {late_time_tmp}:00:00', '%Y-%m-%d %H:%M:%S')
    if not now_time >= early_time or not now_time <= late_time:
        return False
    return True

# 判断多次早安
def judge_have_mor(data, user_id, now_time, interval):
    get_up_time = datetime.datetime.strptime(data[str(user_id)]['get_up_time'], '%Y-%m-%d %H:%M:%S')
    # 上次起床时间和现在时间相差不超过f'{interval}'小时
    if get_up_time + datetime.timedelta(hours = int(interval)) > now_time:
        return True
    return False

# 判断超级亢奋
def judge_super_get_up(data, user_id, now_time, interval):
    sleep_time = datetime.datetime.strptime(data[str(user_id)]['sleep_time'], '%Y-%m-%d %H:%M:%S')
    # 上次睡觉时间和现在时间相差不超过f'{interval}'小时
    if sleep_time + datetime.timedelta(hours = int(interval)) > now_time:
        return True
    return False

# 进行早安并更新数据
def morning_and_update(_current_dir, data, user_id, now_time):
    # 起床并写数据
    sleep_time = datetime.datetime.strptime(data[str(user_id)]['sleep_time'], '%Y-%m-%d %H:%M:%S')
    in_sleep = now_time - sleep_time
    secs = in_sleep.total_seconds()
    day = secs // (3600 * 24)
    hour = (secs - day * 3600 * 24) // 3600
    minute = (secs - day * 3600 * 24 - hour * 3600) // 60
    second = secs - day * 3600 * 24 - hour * 3600 - minute * 60
    # 睡觉时间小于24小时就同时给出睡眠时长
    in_sleep_tmp = 0
    if day == 0:
        in_sleep_tmp = str(int(hour)) + '时' + str(int(minute)) + '分' + str(int(second)) + '秒'
    data[str(user_id)]['get_up_time'] = now_time
    data[str(user_id)]['morning_count'] = int(data[str(user_id)]['morning_count']) + 1
    # 判断是今天第几个起床的
    data['today_count']['morning'] = int(data['today_count']['morning']) + 1
    with open(_current_dir, "w", encoding="UTF-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4, cls=DateEncoder))
    return data['today_count']['morning'], in_sleep_tmp

# 返回早安信息
def get_morning_msg(group_id, user_id, sex_str):
    # 读取配置文件
    current_dir = os.path.join(os.path.dirname(__file__), 'config.json')
    file = open(current_dir, 'r', encoding = 'UTF-8')
    config = json.load(file)

    # 读取早安晚安数据
    _current_dir = os.path.join(os.path.dirname(__file__), f'data\{group_id}.json')
    file = open(_current_dir, 'r', encoding = 'UTF-8')
    data = json.load(file)

    # 若开启规定时间早安，则判断该时间是否允许早安
    now_time = datetime.datetime.now()
    if config['morning']['get_up_intime']['enable']:
        early_time_tmp = config['morning']['get_up_intime']['early_time']
        late_time_tmp = config['morning']['get_up_intime']['late_time']
        if not judge_mor_time(early_time_tmp, late_time_tmp, now_time):
            msg = f'现在不能早安哦，可以早安的时间为{early_time_tmp}时到{late_time_tmp}时'
            return msg

    # 当数据里有过这个人的信息就判断:
    if str(user_id) in list(data.keys()):
        # 若关闭连续多次早安，则判断在设定时间内是否多次早安
        if not config['morning']['multi_get_up']['enable'] and data[str(user_id)]['get_up_time'] != 0:
            interval = config['morning']['multi_get_up']['interval']
            if judge_have_mor(data, user_id, now_time, interval):
                msg = f'{interval}小时内你已经早安过了哦'
                return msg
        # 若关闭超级亢奋，则判断睡眠时长是否小于设定时间
        if not config['morning']['super_get_up']['enable']:
            interval = config['morning']['super_get_up']['interval']
            if judge_super_get_up(data, user_id, now_time, interval):
                msg = f'你可猝死算了吧？现在不能早安哦'
                return msg
        # 若没有说明他还没睡过觉呢
    else:
        msg = '你还没睡过觉呢！不能早安哦'
        return msg

    # 当前面条件均符合的时候，允许早安
    num, in_sleep = morning_and_update(_current_dir, data, user_id, now_time)
    if in_sleep == 0:
        msg = f'早安成功！你是今天第{num}个起床的{sex_str}'
    else:
        msg = f'早安成功！你的睡眠时长为{in_sleep}。\n你是今天第{num}个起床的{sex_str}'
    return msg