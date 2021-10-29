from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image as IMG
from wordcloud import WordCloud, ImageColorGenerator
from dateutil.relativedelta import relativedelta
import pkuseg
import re
import os

import hoshino
from hoshino import Service, priv
from hoshino.typing import CQEvent

from .Sqlite3Manager import execute_sql

sv_help = '''
群/个人词云生成器，记录聊天记录并生成个人/群组词云
在群内发送 我的月内总结/我的年内总结/本群月内总结/本群年内总结 即可
'''.strip()

sv = Service(
    name = '聊天词云',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #可见性
    enable_on_default = True, #默认启用
    bundle = '娱乐', #分组归类
    help_ = sv_help #帮助说明
    )


seg = pkuseg.pkuseg()
PATH = os.path.dirname(os.path.realpath(__file__))


@sv.on_rex(r'^(我的|本群)(月|年)(内|度)?(总结|报告)$')
async def roup_wordcloud_generator(bot, ev):
    uid = ev.user_id
    gid = ev.group_id
    match = ev['match']
    is_my = match.group(1) == '我的'
    is_group = match.group(1) == '本群'
    is_month = match.group(2) == '月'
    is_year = match.group(2) == '年'
    if is_my:
        if is_month:
            msg = await get_review(gid, uid, "month", "member")
        if is_year:
            msg = await get_review(gid, uid, "year", "member")
    elif is_group:
        if is_month:
            msg = await get_review(gid, uid, "month", "group")
        if is_year:
            msg = await get_review(gid, uid, "year", "group")
    else:
        sv.logger.error('聊天词云生成出现错误')
    await bot.send(ev, msg, at_sender=True)


@sv.on_message('group')
async def chat_record(bot, ev):
    uid = ev.user_id
    gid = ev.group_id
    msg = str(ev.message)
    await write_chat_record(seg, gid, uid, msg)


async def count_words(sp, n):
    w = {}
    for i in sp:
        if i not in w:
            w[i] = 1
        else:
            w[i] += 1
    top = sorted(w.items(), key=lambda item: (-item[1], item[0]))
    top_n = top[:n]
    return top_n


async def filter_label(label_list: list) -> list:
    """
    Filter labels

    Args:
        label_list: Words to filter

    Examples:
        result = await filter_label(label_list)

    Return:
        list
    """
    not_filter = ["草"]
    image_filter = "CQ:"
    result = []
    for i in label_list:
        if image_filter in i:
            continue
        elif i in not_filter:
            result.append(i)
        elif len(i) != 1 and i.find('nbsp') < 0:
            result.append(i)
    return result


async def write_chat_record(seg, group_id: int, member_id: int, content: str) -> None:
    content = content.replace("\\", "/")
    filter_words = re.findall(r"\[CQ:(.*?)\]", content, re.S)
    for i in filter_words:
        content = content.replace(f"[CQ:{i}]", "")
    content = content.replace("\"", " ")
    seg_result = seg.cut(content)
    seg_result = await filter_label(seg_result)
    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sql = f"""INSERT INTO chatRecord 
                (`time`, groupId, memberId, content, seg)
                VALUES
                (\"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\", {group_id}, {member_id}, \"{content}\",
                \"{','.join(seg_result)}\") """
    await execute_sql(sql)


async def draw_word_cloud(read_name,uid):
    mask = np.array(IMG.open(f'{PATH}/back.jpg'))
    print(mask.shape)
    wc = WordCloud(
        font_path=f'{PATH}/STKAITI.TTF',
        background_color='white',
        # max_words=500,
        max_font_size=100,
        width=1920,
        height=1080,
        mask=mask
    )
    name = []
    value = []
    for t in read_name:
        name.append(t[0])
        value.append(t[1])
    for i in range(len(name)):
        name[i] = str(name[i])
        # name[i] = name[i].encode('gb2312').decode('gb2312')
    dic = dict(zip(name, value))
    print(dic)
    print(len(dic.keys()))
    wc.generate_from_frequencies(dic)
    image_colors = ImageColorGenerator(mask, default_color=(255, 255, 255))
    print(image_colors.image.shape)
    wc.recolor(color_func=image_colors)
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    # plt.imshow(wc)
    plt.axis("off")
    # plt.show()
    out_img = PATH + '/wordcloud/' + str(uid) +'.png'
    wc.to_file(out_img)


async def get_review(group_id: int, member_id: int, review_type: str, target: str):
    time = datetime.now()
    year, month, day, hour, minute, second = time.strftime("%Y %m %d %H %M %S").split(" ")
    if review_type == "year":
        yearp, monthp, dayp, hourp, minutep, secondp = (time - relativedelta(years=1)).strftime("%Y %m %d %H %M %S").split(" ")
        tag = "年内"
    elif review_type == "month":
        yearp, monthp, dayp, hourp, minutep, secondp = (time - relativedelta(months=1)).strftime("%Y %m %d %H %M %S").split(" ")
        tag = "月内"
    else:
        sv.logger.error('Error: review_type invalid!')
        return "Error: review_type invalid!"

    sql = f"""SELECT * FROM chatRecord 
                    WHERE 
                groupId={group_id} {f'AND memberId={member_id}' if target == 'member' else ''} 
                AND time<'{year}-{month}-{day} {hour}:{minute}:{second}'
                AND time>'{yearp}-{monthp}-{dayp} {hourp}:{minutep}:{secondp}'"""
    # print(sql)
    res = await execute_sql(sql)
    texts = []
    for i in res:
        if i[4]:
            texts += i[4].split(",")
        else:
            texts.append(i[3])
    print(texts)
    top_n = await count_words(texts, 20000)
    await draw_word_cloud(top_n, member_id)
    sql = f"""SELECT count(*) FROM chatRecord 
                    WHERE 
                groupId={group_id} {f'AND memberId={member_id}' if target == 'member' else ''}  
                AND time<'{year}-{month}-{day} {hour}:{minute}:{second}'
                AND time>'{yearp}-{monthp}-{dayp} {hourp}:{minutep}:{secondp}'"""
    res = await execute_sql(sql)
    times = res[0][0]
    msg = f'''
记录时间：
{yearp}-{monthp}-{dayp} {hourp}:{minutep}:{secondp}
---------至---------
{year}-{month}-{day} {hour}:{minute}:{second}
自有记录以来，{'你' if target == 'member' else '本群'}一共发了{times}条消息
下面是{'你的' if target == 'member' else '本群的'}{tag}词云:
[CQ:image,file=file:///{PATH}/wordcloud/{member_id}.png]
'''.strip()
    return msg
