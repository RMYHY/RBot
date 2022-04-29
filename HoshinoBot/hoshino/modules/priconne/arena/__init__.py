import re
import time
import asyncio
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

import hoshino
from hoshino import Service, R
from hoshino.typing import *
from hoshino.util import FreqLimiter, concat_pic, pic2b64, silence

from .. import chara

from os.path import dirname, join, exists
import numpy as np
import json
from io import BytesIO
import requests
import copy



import cv2

sv_help = '''
[怎么拆] 接防守队角色名 查询竞技场解法
[点赞] 接作业id 评价作业
[点踩] 接作业id 评价作业
'''.strip()
sv = Service('pcr-arena', help_=sv_help, bundle='pcr查询')

from . import arena

lmt = FreqLimiter(5)

aliases = ('怎么拆', '怎么解', '怎么打', '如何拆', '如何解', '如何打', 'jjc查询')
aliases_b = tuple('b' + a for a in aliases) + tuple('B' + a for a in aliases)
aliases_b = list(aliases_b)
aliases_b.append('bjjc')
aliases_b = tuple(aliases_b)
aliases_tw = tuple('台' + a for a in aliases)
aliases_tw = list(aliases_tw)
aliases_tw.append('台jjc')
aliases_tw = tuple(aliases_tw)
aliases_jp = tuple('日' + a for a in aliases)
aliases_jp = list(aliases_jp)
aliases_jp.append('日jjc')
aliases_jp = tuple(aliases_jp)

try:
    thumb_up_i = R.img('priconne/gadget/thumb-up-i.png').open().resize((16, 16), Image.LANCZOS)
    thumb_up_a = R.img('priconne/gadget/thumb-up-a.png').open().resize((16, 16), Image.LANCZOS)
    thumb_down_i = R.img('priconne/gadget/thumb-down-i.png').open().resize((16, 16), Image.LANCZOS)
    thumb_down_a = R.img('priconne/gadget/thumb-down-a.png').open().resize((16, 16), Image.LANCZOS)
except Exception as e:
    sv.logger.exception(e)


@sv.on_prefix(aliases)
async def arena_query(bot, ev):
    await _arena_query(bot, ev, region=1)


@sv.on_prefix(aliases_b)
async def arena_query_b(bot, ev):
    await _arena_query(bot, ev, region=2)


@sv.on_prefix(aliases_tw)
async def arena_query_tw(bot, ev):
    await _arena_query(bot, ev, region=3)


@sv.on_prefix(aliases_jp)
async def arena_query_jp(bot, ev):
    await _arena_query(bot, ev, region=4)


def render_atk_def_teams(entries, border_pix=5):
    n = len(entries)
    icon_size = 64
    im = Image.new('RGBA', (5 * icon_size + 100, n * (icon_size + border_pix) - border_pix), (255, 255, 255, 255))
    font = ImageFont.truetype('msyh.ttc', 16)
    draw = ImageDraw.Draw(im)
    for i, e in enumerate(entries):
        y1 = i * (icon_size + border_pix)
        y2 = y1 + icon_size
        for j, c in enumerate(e['atk']):
            #print(c)
            icon = c.render_icon(icon_size)
            x1 = j * icon_size
            x2 = x1 + icon_size
            im.paste(icon, (x1, y1, x2, y2), icon)
        thumb_up = thumb_up_a if e['user_like'] > 0 else thumb_up_i
        thumb_down = thumb_down_a if e['user_like'] < 0 else thumb_down_i
        x1 = 5 * icon_size + 10
        x2 = x1 + 16
        im.paste(thumb_up, (x1, y1 + 12, x2, y1 + 28), thumb_up)
        im.paste(thumb_down, (x1, y1 + 39, x2, y1 + 55), thumb_down)
        #draw.text((x1, y1), e['qkey'], (0, 0, 0, 255), font)
        draw.text((x1 + 25, y1 + 10), f"{e['up']}", (0, 0, 0, 255), font)
        #draw.text((x1+25, y1+35), f"{e['down']}+{e['my_down']}" if e['my_down'] else f"{e['down']}", (0, 0, 0, 255), font)
        draw.text((x1 + 25, y1 + 35), f"{e['down']}", (0, 0, 0, 255), font)
    return im


def getBox(img):
    img = img.convert("RGBA")
    # img = img.resize((int(img.width / img.height * 1000), 1000), Image.ANTIALIAS)
    '''
    xpos, ypos = getPos(img)
    print(xpos, ypos)
    if xpos == [] or ypos == []:
        return [], []
    boxDict, s = getUnit(img, xpos, ypos)
    '''
    boxDict, s = getPos(img)
    return boxDict, s


curpath = dirname(__file__)

dataDir = join(curpath, 'dic.npy')
data = np.load(dataDir, allow_pickle=True).item()


def getBoxPos(uid):
    if uid >= 1000 and uid <= 1156:
        return uid - 1000  #0-157
    elif uid >= 1701 and uid <= 1702:
        return uid - 1544  # 157-158
    elif uid >= 1801 and uid <= 1805:
        return uid - 1642  # 159-163
    return 0


def cut_image(image, hash_size=16):
    # 将图像缩小成(16+1)*16并转化成灰度图
    image1 = image.resize((hash_size + 1, hash_size), Image.ANTIALIAS).convert('L')
    pixel = list(image1.getdata())
    return pixel


def trans_hash(lists):
    # 比较列表中相邻元素大小
    j = len(lists) - 1
    hash_list = []
    m, n = 0, 1
    for i in range(j):
        if lists[m] > lists[n]:
            hash_list.append(1)
        else:
            hash_list.append(0)
        m += 1
        n += 1
    return hash_list


def difference_value(image_lists):
    # 获得图像差异值并获得指纹
    assert len(image_lists) == 17 * 16, "size error"
    m, n = 0, 17
    hash_list = []
    for i in range(0, 16):
        slc = slice(m, n)
        image_slc = image_lists[slc]
        hash_list.append(trans_hash(image_slc))
        m += 17
        n += 17
    return hash_list


def calc_distance(image1, image2):
    image1_lists = cut_image(image1)
    image2_lists = cut_image(image2)
    hash_lists1 = difference_value(image1_lists)
    hash_lists2 = difference_value(image2_lists)
    calc = abs(np.array(hash_lists2) - np.array(hash_lists1))
    calc = sum(sum(calc))
    return calc


#def getPos(img):
#    img = np.array(img)
#    x, y, z = img.shape
#    #print(x,y,z)
#    last = 0
#    now = 0
#
#    xpos = []
#    for i in range(1, x, 1):
#        #print(i)
#        cnt = 0
#        white = 0
#        totcnt = 0
#        for j in range(1, y, 11):
#            if sum(img[i][j]) >= 700:
#                totcnt += 1
#                if white == 0:
#                    white = 1
#                    cnt += 1
#            elif white == 1:
#                white = 0
#
#        if totcnt >= x / 20 and cnt >= 1 and cnt <= 5:
#            now = 1
#        else:
#            now = -1
#
#        if last == 1 and now == -1:
#            #print(i, cnt, totcnt, "白→彩")
#            if len(xpos) and type(xpos[-1]) == int:
#                xpos = xpos[:-1]
#            xpos.append(i)
#        elif last == -1 and now == 1:
#            #print(i, cnt, totcnt, "彩→白")
#            if len(xpos) and type(xpos[-1]) == int:
#                if i - xpos[-1] >= 100:
#                    xpos[-1] = (xpos[-1], i)
#                else:
#                    xpos = xpos[:-1]
#                if len(xpos) >= 3:
#                    break
#        last = now
#
#    if len(xpos) and type(xpos[-1]) == int:
#        xpos = xpos[:-1]
#    if len(xpos) == 0:
#        return [], []  # 报错 退出
#
#    ypos = []
#    for i in range(1, y, 1):
#        #print(i)
#        cnt = 0
#        white = 0
#        totcnt = 0
#        for j in range(xpos[0][0], xpos[0][1], 11):
#            if sum(img[j][i]) >= 700:
#                totcnt += 1
#                if white == 0:
#                    white = 1
#                    cnt += 1
#            elif white == 1:
#                white = 0
#
#        if totcnt >= (xpos[0][1] - xpos[0][0]) * 0.8 / 11 and cnt <= 2:
#            now = 1
#        else:
#            now = -1
#        if last == 1 and now == -1:
#            ypos.append(i)
#        elif last == -1 and now == 1:
#            if len(ypos) and type(ypos[-1]) == int:
#                if i - ypos[-1] >= 100:
#                    ypos[-1] = (ypos[-1], i)
#                else:
#                    ypos = ypos[:-1]
#                if len(ypos) >= 10:
#                    break
#        last = now
#    return xpos, ypos


def cutting(img, mode):
    im_grey = img.convert('L')
    totArea = (im_grey.size)[0] * (im_grey.size)[1]
    im_grey = im_grey.point(lambda x: 255 if x > 210 else 0)
    thresh = np.array(im_grey)

    ######cv2.findContours. opencv3版本会返回3个值，opencv2和4只返回后两个值
    #img2, contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    img2 = thresh

    lis = []
    icon = []
    icon_area = {}
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])  #计算轮廓面积，但是可能和像素点区域不太一样 收藏
        lis.append(area)
        if area > 500:
            if mode == 2:
                x, y, w, h = cv2.boundingRect(contours[i])
                if w / h > 0.95 and w / h < 1.05:
                    are = (w + h) // 2
                    areaRatio = are * are / totArea * 100
                    #print(f"{areaRatio:2f}%")
                    if areaRatio >= 0.5:
                        icon.append([are, [x, y, w, h]])
                        icon_area[are] = icon_area.setdefault(are, 0) + 1
    #print()
    if mode == 1:
        i = lis.index(max(lis))
        x, y, w, h = cv2.boundingRect(contours[i])
        #cv2.rectangle(img2, (x, y), (x + w, y + h), (153, 153, 0), 5)
        img3 = img2[y + 2:y + h - 2, x + 2:x + w - 2]
        return Image.fromarray(img3), [x, y, w, h]
    if mode == 2:
        if icon_area == {}:
            return False
        icon_area = sorted(icon_area.items(), key=lambda x: x[1], reverse=True)
        #print(icon_area)
        accepted_area = [icon_area[0][0]]
        for i in icon_area:
            if abs(i[0] - accepted_area[0]) <= 5:
                accepted_area.append(i[0])
        #print(accepted_area)
        icon = list(sorted(map(lambda x: x[1], filter(lambda x: x[0] in accepted_area, icon)), key=lambda x: x[1] * 100000 + x[0]))
        #print(icon)
        return icon


def cut(img, border):
    x, y, w, h = border
    img = np.array(img)
    img = img[y + 2:y + h - 2, x + 2:x + w - 2]
    img = Image.fromarray(img)
    return img


def getPos(img):
    im_grey = img
    cnt = 0
    while cnt <= 5:
        bo = False
        cnt += 1
        border = cutting(im_grey, 2)
        if border == False:
            bo = True
        else:
            border = sorted(border, key=lambda x: x[0] * 10000 + x[1])
            xpos = 1
            xlast = border[0][0]
            ypos = 1
            ylast = border[0][1]
            outpDict = {}
            for i in border:
                x, y, w, h = i
                if y / ylast > 1.1:
                    ypos += 1
                elif x / xlast > 1.1:
                    ypos = 1
                    xpos += 1
                xlast = x
                ylast = y
                cropped = img.crop([x + 2, y + 2, x + w - 2, y + h - 2])
                unit_id, unit_name = getUnit(cropped)
                if unit_name == "Unknown" or unit_id == 0:
                    pass
                else:
                    if ypos in outpDict:
                        outpDict[ypos].append([unit_id, unit_name])
                    else:
                        outpDict[ypos] = [[unit_id, unit_name]]
            if len(border) >= 5:
                outpDict = list(sorted(outpDict.items(), key=lambda x: x[0]))
                outpList = []
                outpName = []
                for i in outpDict:
                    i = i[1]
                    if len(i) >= 5:
                        i = i[-5:]
                        lis = []
                        nam = []
                        for j in i:
                            lis.append(j[0])
                            nam.append(j[1])
                        outpList.append(copy.deepcopy(lis))
                        outpName.append(' '.join(nam))
                #print(outpList)
                outpName = "识别阵容为：\n" + '\n'.join(outpName)
                #print(outpName)
                return outpList, outpName

        im_grey, border = cutting(im_grey, 1)
        if cnt == 1 or bo:
            im_grey = im_grey.point(lambda x: 0 if x > 128 else 255)
        img = cut(img, border)
    return [], []

def getUnit(img2):
    img2 = img2.convert("RGB").resize((128, 128), Image.ANTIALIAS)
    #img2.show()
    img3 = np.array(img2)
    #img4 = img3[21:105, 3:124, :]
    img4 = img3[25:96, 8:97, :]
    img4 = Image.fromarray(img4)
    #img4.show()
    dic = {}
    for uid in data:
        #icon = Image.fromarray(data[uid][21:105, 3:124, :])
        icon = Image.fromarray(data[uid][25:96, 8:97, :])
        dic[uid] = calc_distance(icon, img4)
    lis = list(sorted(dic.items(), key=lambda x: abs(x[1])))
    if int(lis[0][1]) <= 92:
        uid = int(lis[0][0]) // 100
        if int(lis[0][0]) == 108231 and int(lis[1][0]) == 100731 and int(lis[1][1]) - int(lis[0][1]) <= 5:
            uid = 1007
        try:
            nam = CHARA_NAME[uid]
            return uid, nam
        except:
            return uid, "Unknown"
    return 0, "Unknown"


#def getUnit(img2, xpos, ypos):
#'''
#识别阵容为：
#真步 凯留(夏日) 似似花 可可萝 贪吃佩可
#咲恋(夏日) 怜 日和 可可萝(新年) 怜(新年)
#
#[[1010, 1078, 1070, 1059, 1058], [1103, 1003, 1001, 1119, 1089]]
#'''
#
#    iconCnt = 0
#    boxDict = []
#    soutp = ""
#    outp = "识别阵容为：\n"
#    for x in xpos:
#        smallDict = []
#        ssoutp = []
#        for y in ypos:
#            img3 = img2.crop((y[0], x[0], y[1], x[1])).resize((144, 144), Image.ANTIALIAS).crop((8, 8, 136, 136))
#            img5 = img3
#            img3 = np.array(img3)
#            img4 = img3[21:105, 3:124, :]
#            # print(int(np.mean(img4.flatten())))
#            if int(np.mean(img4.flatten())) >= 230:
#                continue
#            iconCnt += 1
#            img4 = Image.fromarray(img4)
#            #img4.show()
#            dic = {}
#            for uid in data:
#                icon = Image.fromarray(data[uid][21:105, 3:124, :])
#                dic[uid] = calc_distance(icon, img4)
#            lis = list(sorted(dic.items(), key=lambda x: abs(x[1])))
#            if int(lis[0][1]) <= 92:
#                # print("icon%-2d : " % (iconCnt), lis[:5])
#                soutp += "icon%-2d : " % (iconCnt)
#                uid = int(lis[0][0]) // 100
#                if int(lis[0][0]) == 108231 and int(lis[1][0]) == 100731 and int(lis[1][1]) - int(lis[0][1]) <= 5:
#                    uid = 1007
#                smallDict.append(uid)
#                nam = CHARA_NAME[uid]
#                ssoutp.append(nam)
#                soutp += nam + " "
#                # img5.save(f"icon{iconCnt}_{uid}_{nam}.jpg")
#                if int(lis[1][1]) - int(lis[0][1]) <= 5 and int(lis[1][0]) // 100 != int(lis[0][0]) // 100:
#                    soutp += " 低置信度"
#                soutp += "\n"
#            else:
#                iconCnt -= 1
#        smallDict = smallDict[-5:]
#        ssoutp = ssoutp[-5:]
#        outp += ' '.join(ssoutp) + "\n"
#        boxDict.append(smallDict)
#
#    return boxDict, outp


def get_pic(address):
    return requests.get(address, timeout=20).content


async def _arena_query(bot, ev: CQEvent, region: int):
    arena.refresh_quick_key_dic()
    uid = ev.user_id

    if not lmt.check(uid):
        await bot.finish(ev, '您查询得过于频繁，请稍等片刻', at_sender=True)
    lmt.start_cd(uid)

    # 处理输入数据
    defen = ""
    ret = re.match(r"\[CQ:image,file=(.*),url=(.*)\]", str(ev.message))
    if ret:
        await bot.send(ev, "recognizing")
        image = Image.open(BytesIO(get_pic(ret.group(2))))
        boxDict, s = getBox(image)
        if boxDict == []:
            await bot.finish(ev, "未识别到角色！")
        print(s)
        print(boxDict)
        try:
            await bot.send(ev, s)
        except:
            pass
        lis = []  # [[[第1队第1解],[第1队第2解]], [[第2队第1解]], []]
        if len(boxDict) == 1:
            await __arena_query(bot, ev, region, boxDict[0])
            return
        if len(boxDict) > 3:
            await bot.finish(ev, "请截图pjjc详细对战记录（对战履历详情）（含敌我双方2或3队阵容）")
        tot = 0
        for i in boxDict:
            li = []
            res = await __arena_query(bot, ev, region, i, 1)
            #print(res)
            if res == []:
                lis.append([])
            else:
                tot += 1
                for num, squad in enumerate(res):
                    soutp = ""
                    squads = []
                    for nam in squad["atk"]:
                        #print(nam)
                        soutp += nam.name + " "
                        squads.append(nam.id)
                    #squads.append(int(squad["up"]) - int(squad["down"]))
                    squads.append(num)
                    squads.append(soutp[:-1])
                    li.append(copy.deepcopy(squads))
                lis.append(copy.deepcopy(li))
            await asyncio.sleep(2)
        print(lis)
        if tot == 0:
            await bot.finish(ev, "均未查询到解法！")
        if tot == 1:
            for num, i in enumerate(lis):
                if len(i) > 0:
                    await bot.send(ev, f"仅第{num+1}队查询到解法！")
                    await __arena_query(bot, ev, region, boxDict[num])
            return
        le = len(lis)
        outp = ""
        cnt = 0
        if le == 3:
            s1 = lis[0]
            s2 = lis[1]
            s3 = lis[2]
            for x in s1:
                for y in s2:
                    for z in s3:
                        temp = x[:-2] + y[:-2] + z[:-2]
                        if len(temp) == len(set(temp)):
                            cnt += 1
                            if cnt <= 8:
                                outp += f"优先级：{x[-2]+y[-2]+z[-2]:02d}\n第{1}队：{x[-1]}\n第{2}队：{y[-1]}\n第{3}队：{z[-1]}\n"
        if outp != "":
            outp = "三队无冲配队：\n" + outp
            await bot.finish(ev, outp)
        for i in range(le - 1):
            for j in range(i + 1, le):
                s1 = lis[i]
                s2 = lis[j]
                for x in s1:
                    for y in s2:
                        if not (set(x[:-2]) & set(y[:-2])):
                            cnt += 1
                            if cnt < 8:
                                outp += f"优先级：{x[-2]+y[-2]:02d}\n第{i+1}队：{x[-1]}\n第{j+1}队：{y[-1]}\n"
        if outp != "":
            outp = "两队无冲配队：\n" + outp
            await bot.finish(ev, outp)
        outp = "不存在无冲配队！"
        for num, i in enumerate(lis):
            if i != []:
                outp += f"\n第{num+1}队的解法为：\n"
                for j in i:
                    outp += j[-1] + "\n"
        await bot.finish(ev, outp)

    else:
        await __arena_query(bot, ev, region)


async def __arena_query(bot, ev: CQEvent, region: int, defen="", raw=0):
    uid = ev.user_id
    unknown = ""
    if defen == "":
        defen = ev.message.extract_plain_text()
        defen = re.sub(r'[?？，,_]', '', defen)
        defen, unknown = chara.roster.parse_team(defen)

    if unknown:
        _, name, score = chara.guess_id(unknown)
        if score < 70 and not defen:
            return  # 忽略无关对话
        msg = f'无法识别"{unknown}"' if score < 70 else f'无法识别"{unknown}" 您说的有{score}%可能是{name}'
        await bot.finish(ev, msg)
    if not defen:
        await bot.finish(ev, '查询请发送"b/日/台jjc+防守队伍"，无需+号', at_sender=True)
    if len(defen) > 5:
        await bot.finish(ev, '编队不能多于5名角色', at_sender=True)
    if len(defen) < 5:
        await bot.finish(ev, '由于数据库限制，少于5名角色的检索条件请移步pcrdfans.com进行查询', at_sender=True)
    if len(defen) != len(set(defen)):
        await bot.finish(ev, '编队中含重复角色', at_sender=True)
    if any(chara.is_npc(i) for i in defen):
        await bot.finish(ev, '编队中含未实装角色', at_sender=True)
    if 1004 in defen:
        await bot.send(ev, '\n⚠️您正在查询普通版炸弹人\n※万圣版可用万圣炸弹人/瓜炸等别称', at_sender=True)

    #print(defen)
    # 执行查询
    sv.logger.info('Doing query...')
    res = None
    try:
        res = await arena.do_query(defen, uid, region, raw)
    except hoshino.aiorequests.HTTPError as e:
        code = e.response["code"]
        if code == 117:
            await bot.finish(ev, "高峰期服务器限流！请前往pcrdfans.com/battle")
        else:
            await bot.finish(ev, f'code{code} 查询出错\n请先前往pcrdfans.com进行查询', at_sender=True)
    sv.logger.info('Got response!')

    # 处理查询结果
    if res is None:
        if not raw:
            await bot.finish(ev, '数据库未返回数据，请再次尝试查询或前往pcrdfans.com', at_sender=True)
        else:
            return []
    if not len(res):
        if not raw:
            await bot.finish(ev, '抱歉没有查询到解法\n作业上传请前往pcrdfans.com', at_sender=True)
        else:
            return []
    res = res[:min(8, len(res))]  # 限制显示数量，截断结果
    if raw:
        return res
    # print(res)

    # 发送回复
    sv.logger.info('Arena generating picture...')
    teams = render_atk_def_teams(res)
    teams = pic2b64(teams)
    teams = MessageSegment.image(teams)
    sv.logger.info('Arena picture ready!')
    # 纯文字版
    # atk_team = '\n'.join(map(lambda entry: ' '.join(map(lambda x: f"{x.name}{x.star if x.star else ''}{'专' if x.equip else ''}" , entry['atk'])) , res))

    # details = [" ".join([
    #     f"赞{e['up']}+{e['my_up']}" if e['my_up'] else f"赞{e['up']}",
    #     f"踩{e['down']}+{e['my_down']}" if e['my_down'] else f"踩{e['down']}",
    #     e['qkey'],
    #     "你赞过" if e['user_like'] > 0 else "你踩过" if e['user_like'] < 0 else ""
    # ]) for e in res]

    # defen = [ chara.fromid(x).name for x in defen ]
    # defen = f"防守方【{' '.join(defen)}】"
    at = str(MessageSegment.at(ev.user_id))

    msg = [
        # defen,
        f'已为骑士{at}查询到以下进攻方案：',
        str(teams),
        # '作业评价：',
        # *details,
        # '※发送"点赞/点踩"可进行评价'
    ]
    if region == 1:
        msg.append('※使用"b怎么拆"或"台怎么拆"可按服过滤')
    msg.append('https://www.pcrdfans.com/battle')

    sv.logger.debug('Arena sending result...')
    await bot.send(ev, '\n'.join(msg))
    sv.logger.debug('Arena result sent!')

    if ev.group_id == 1017321923:
        await silence(ev, 5 * 60)


# @sv.on_prefix('点赞')
async def arena_like(bot, ev):
    await _arena_feedback(bot, ev, 1)


# @sv.on_prefix('点踩')
async def arena_dislike(bot, ev):
    await _arena_feedback(bot, ev, -1)


rex_qkey = re.compile(r'^[0-9a-zA-Z]{5}$')


async def _arena_feedback(bot, ev: CQEvent, action: int):
    action_tip = '赞' if action > 0 else '踩'
    qkey = ev.message.extract_plain_text().strip()
    if not qkey:
        await bot.finish(ev, f'请发送"点{action_tip}+作业id"，如"点{action_tip}ABCDE"，不分大小写', at_sender=True)
    if not rex_qkey.match(qkey):
        await bot.finish(ev, f'您要点{action_tip}的作业id不合法', at_sender=True)
    try:
        await arena.do_like(qkey, ev.user_id, action)
    except KeyError:
        await bot.finish(ev, '无法找到作业id！您只能评价您最近查询过的作业', at_sender=True)
    await bot.send(ev, '感谢您的反馈！', at_sender=True)


@sv.on_command('arena-upload', aliases=('上传作业', '作业上传', '上傳作業', '作業上傳'))
async def upload(ss: CommandSession):
    atk_team = ss.get('atk_team', prompt='请输入进攻队+5个表示星级的数字+5个表示专武的0/1 无需空格')
    def_team = ss.get('def_team', prompt='请输入防守队+5个表示星级的数字+5个表示专武的0/1 无需空格')
    if 'pic' not in ss.state:
        ss.state['pic'] = MessageSegment.image(pic2b64(concat_pic([
            chara.gen_team_pic(atk_team),
            chara.gen_team_pic(def_team),
        ])))
    confirm = ss.get('confirm', prompt=f'{ss.state["pic"]}\n{MessageSegment.at(ss.event.user_id)}确认上传？\n> 确认\n> 取消')
    # TODO: upload
    await ss.send('假装上传成功了...')


@upload.args_parser
async def _(ss: CommandSession):
    if ss.is_first_run:
        await ss.send('我将帮您上传作业至pcrdfans，作业将注明您的昵称及qq。您可以随时发送"算了"或"取消"终止上传。')
        await asyncio.sleep(0.5)
        return
    arg = ss.current_arg_text.strip()
    if arg == '算了' or arg == '取消':
        await ss.finish('已取消上传')

    if ss.current_key.endswith('_team'):
        if len(arg) < 15:
            return
        team, star, equip = arg[:-10], arg[-10:-5], arg[-5:]
        if not re.fullmatch(r'[1-6]{5}', star):
            await ss.pause('请依次输入5个数字表示星级，顺序与队伍相同')
        if not re.fullmatch(r'[01]{5}', equip):
            await ss.pause('请依次输入5个0/1表示专武，顺序与队伍相同')
        star = [int(s) for s in star]
        equip = [int(s) for s in equip]
        team, unknown = chara.roster.parse_team(team)
        if unknown:
            _, name, score = chara.guess_id(unknown)
            await ss.pause(f'无法识别"{unknown}"' if score < 70 else f'无法识别"{unknown}" 您说的有{score}%可能是{name}')
        if len(team) != 5:
            await ss.pause('队伍必须由5个角色组成')
        ss.state[ss.current_key] = [chara.fromid(team[i], star[i], equip[i]) for i in range(5)]
    elif ss.current_key == 'confirm':
        if arg == '确认' or arg == '確認':
            ss.state[ss.current_key] = True
    else:
        raise ValueError
    return


CHARA_NAME = {
    1000: "未知角色",
    1001: "日和",
    1002: "优衣",
    1003: "怜",
    1004: "禊",
    1005: "茉莉",
    1006: "茜里",
    1007: "宫子",
    1008: "雪",
    1009: "杏奈",
    1010: "真步",
    1011: "璃乃",
    1012: "初音",
    1013: "七七香",
    1014: "霞",
    1015: "美里",
    1016: "铃奈",
    1017: "香织",
    1018: "伊绪",
    1020: "美美",
    1021: "胡桃",
    1022: "依里",
    1023: "绫音",
    1025: "铃莓",
    1026: "铃",
    1027: "惠理子",
    1028: "咲恋",
    1029: "望",
    1030: "妮诺",
    1031: "忍",
    1032: "秋乃",
    1033: "真阳",
    1034: "优花梨",
    1036: "镜华",
    1037: "智",
    1038: "栞",
    1040: "碧",
    1042: "千歌",
    1043: "真琴",
    1044: "伊莉亚",
    1045: "空花",
    1046: "珠希",
    1047: "纯",
    1048: "美冬",
    1049: "静流",
    1050: "美咲",
    1051: "深月",
    1052: "莉玛",
    1053: "莫妮卡",
    1054: "纺希",
    1055: "步未",
    1056: "流夏",
    1057: "吉塔",
    1058: "贪吃佩可",
    1059: "可可萝",
    1060: "凯留",
    1061: "矛依未",
    1063: "亚里莎",
    1065: "嘉夜",
    1066: "祈梨",
    1067: "穗希",
    1068: "拉比林斯达",
    1069: "真那",
    1070: "似似花",
    1071: "克莉丝提娜",
    1072: "可萝爹",
    1073: "拉基拉基",
    1075: "贪吃佩可(夏日)",
    1076: "可可萝(夏日)",
    1077: "铃莓(夏日)",
    1078: "凯留(夏日)",
    1079: "珠希(夏日)",
    1080: "美冬(夏日)",
    1081: "忍(万圣节)",
    1082: "宫子(万圣节)",
    1083: "美咲(万圣节)",
    1084: "千歌(圣诞节)",
    1085: "胡桃(圣诞节)",
    1086: "绫音(圣诞节)",
    1087: "日和(新年)",
    1088: "优衣(新年)",
    1089: "怜(新年)",
    1090: "惠理子(情人节)",
    1091: "静流(情人节)",
    1092: "安",
    1093: "露",
    1094: "古蕾娅",
    1095: "空花(大江户)",
    1096: "妮诺(大江户)",
    1097: "雷姆",
    1098: "拉姆",
    1099: "爱蜜莉雅",
    1100: "铃奈(夏日)",
    1101: "伊绪(夏日)",
    1103: "咲恋(夏日)",
    1104: "真琴(夏日)",
    1105: "香织(夏日)",
    1106: "真步(夏日)",
    1107: "碧(插班生)",
    1108: "克萝依",
    1109: "琪爱儿",
    1110: "优妮",
    1111: "镜华(万圣节)",
    1112: "禊(万圣节)",
    1113: "美美(万圣节)",
    1114: "露娜",
    1115: "克莉丝提娜(圣诞节)",
    1116: "望(圣诞节)",
    1117: "伊莉亚(圣诞节)",
    1119: "可可萝(新年)",
    1120: "凯留(新年)",
    1121: "铃莓(新年)",
    1122: "霞(魔法少女)",
    1123: "栞(魔法少女)",
    1124: "卯月(偶像大师)",
    1125: "凛(偶像大师)",
    1126: "未央(偶像大师)",
    1127: "铃(游侠)",
    1128: "真阳(游侠)",
    1129: "璃乃(奇境)",
    1130: "步未(奇境)",
    1131: "流夏(夏日)",
    1132: "杏奈(夏日)",
    1133: "七七香(夏日)",
    1134: "初音(夏日)",
    1135: "美里(夏日)",
    1136: "纯(夏日)",
    1137: "茜里(天使)",
    1138: "依里(天使)",
    1139: "纺希(万圣节)",
    1140: "怜(万圣节)",
    1141: "茉莉(万圣节)",
    1142: "莫妮卡(魔法少女)",
    1143: "智(魔法少女)",
    1144: "秋乃(圣诞节)",
    1145: "咲恋(圣诞节)",
    1146: "优花梨(圣诞节)",
    1147: "矛依未(新年)",
    1150: "似似花(新年)",
    1155: "可可萝(仪装束)",
    1156: "优衣(仪装束)",
    1701: "环奈",
    1702: "环奈(振袖)",
    1801: "日和(公主)",
    1802: "优衣(公主)",
    1804: "贪吃佩可(公主)",
    1805: "可可萝(公主)"
}