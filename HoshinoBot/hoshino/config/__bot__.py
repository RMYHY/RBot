# hoshino监听的端口与ip
PORT = 8090
HOST = '127.0.0.1'      # 本地部署使用此条配置（QQ客户端和bot端运行在同一台计算机）
# HOST = '0.0.0.0'      # 开放公网访问使用此条配置（不安全）

DEBUG = False           # 调试模式

SUPERUSERS = [549883020,1061301935]     # 填写超级用户的QQ号，可填多个用半角逗号","隔开
NICKNAME = 'bot', 'hina', '氷川日菜'           # 机器人的昵称。呼叫昵称等同于@bot，可用元组配置多个昵称

COMMAND_START = {''}    # 命令前缀（空字符串匹配任何消息）
COMMAND_SEP = set()     # 命令分隔符（hoshino不需要该特性，保持为set()即可）

USE_CQPRO = True       # 是否使用Pro版酷Q功能(此项参数在原生HoshinoBot已经去除，但部分第三方插件需要此参数)

# 发送图片的协议
# 可选 http, file, base64
# 当QQ客户端与bot端不在同一台计算机时，可用http协议
RES_PROTOCOL = 'file'
# 资源库文件夹，需可读可写，windows下注意反斜杠转义
RES_DIR = r'C:/Resources/'
# 使用http协议时需填写，原则上该url应指向RES_DIR目录
RES_URL = 'http://127.0.0.1:5000/C:/Resources/'


# 启用的模块
# 初次尝试部署时请先保持默认
# 如欲启用新模块，请认真阅读部署说明，逐个启用逐个配置
# 切忌一次性开启多个
MODULES_ON = {
    'anticoncurrency',  #反并发
    'aircon',           #模拟空调
    'asill',            #发病小作文
    #'authMS',          #授权管理
    'bangguess',        #猜邦邦（BanG Dream头像）
    'blacklist',        #黑名单
    'bilidynamicpush',  #b站动态推送
    'botchat',          #语言库
    'botmanage',        #功能管理
    'clanrank',         #公会排名
    'chachengfen',      #查成分B站关注列表
    #'check',            #服务器状态查询
    'dice',             #骰子
    #'epixiv',          #P站搜图（未配置）
    'eqa',              #问答
    'explosion',        #爆裂魔法
    'flac',             #无损音乐
    'generator-image',  #表情包生成器
    'generator-text',   #文章生成器
    'good_morning',     #早安晚安
    'groupmaster',      #群管理
    'guess-icon',       #猜头像（pcr头像）
    'guess-text',       #猜角色（pcr描述）
    'hedao',            #合刀计算
    'HELP',             #指令列表帮助
    'hiumsentences',    #网抑云生成器
    'hourcall',         #整点时报
    #'laopo',            #群老婆
    'memberguess',      #猜群友（群员头像）
    'music',            #点歌
    'nowtime',          #报时
    'pcractualguess',   #猜现实（pcr现实）
    'pcr_calendar',     #pcr日程
    'pcr-rank',         #rank表
    'pcrclanbattle',    #会战功能
    'pcrmiddaymusic',   #午间音乐
    'pcrwarn',          #pcr提醒（任务、买药、jjc）
    'pcrsealkiller',    #海豹杀手
    'priconne',         #实用功能集合
    #四格漫画推送，新闻推送，竞技场查询，模拟赛跑，模拟抽卡，贵族决斗
    'record',           #pcr角色语音
    'report-hoshino',   #会战报告-Hoshino版
    'report-yobot',     #会战报告-Yobot版
    'revgif',           #GIF倒放
    'russian',          #俄罗斯轮盘
    'search-image',     #搜图
    'setu',             #离线色图
    #'setu_renew',      #在线色图（未更新）
    'shaojo',           #今天是什么少女
    'traceanime',       #搜番
    'translate',        #翻译
    'voiceguess',       #猜语音
    'vtbguess',         #猜vtb/vup头像
    'weather',          #天气
    'whattoeat',        #今天吃什么
    #'wordcloud',       #词云
}
