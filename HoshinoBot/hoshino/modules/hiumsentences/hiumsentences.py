import requests,random,os,json
from hoshino import Service, R
from hoshino.typing import CQEvent
from hoshino.util import FreqLimiter
import hoshino
sv = Service('hiumsentences', enable_on_default=True, visible=True,help_='''
[网抑云时间] 来点网抑云语录
'''.strip())

_time_limit = 5
_lmt = FreqLimiter(_time_limit)

def pic_gender_cqcode(dic_name):
    '''
    获得/res/img/dic_name目录下一张随机图片，返回cqcode
    '''
    pic_dir = R.img(dic_name).path
    
    file_list:list = os.listdir(pic_dir)
    img_random = random.choice(file_list)
    img_path = dic_name + '/' + img_random
    img_cqcode = R.img(str(img_path)).cqcode
    return img_cqcode

def get_nt_words():
    _path = os.path.join(os.path.dirname(__file__), 'nt_words.json')
    if os.path.exists(_path):
        with open(_path,"r",encoding='utf-8') as dump_f:
            try:
                # 读取错误一般是人工改动了config并且导致json格式错误
                words = json.load(dump_f)
            except Exception as e:
                hoshino.logger.error(f'读取网抑云语录时发生错误{type(e)}')
                return None
    else:
        hoshino.logger.error(f'目录下未找到网抑云语录')
    keys = list(words.keys())
    key = random.choice(keys)

    return words[key]["text"]


@sv.on_keyword(('上号','生而为人','生不出人','网抑云','已黑化','到点了'))
async def net_ease_cloud_word(bot,ev:CQEvent):
    gid = ev.group_id
    if not _lmt.check(gid):
        # 冲太多...哦不是, 抑郁太多对身体不好
        return
    _lmt.start_cd(gid)
    try:
        sentences = pic_gender_cqcode('chat/网抑云')
    except Exception as e:
        hoshino.logger.error(f'获取目录res/img/chat/网抑云下的图片时发生错误{type(e)}, 请检查')
        sentences = ''
    
    nt_word = get_nt_words()
    sentences += nt_word
    await bot.send(ev, sentences)

    