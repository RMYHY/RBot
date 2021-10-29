# RBot

基于[Go-cqhttp](https://github.com/Mrs4s/go-cqhttp)，[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)，[Yobot](http://yobot.win/)的**QQ群机器人**

本机器人以[Mirai-Bot](https://github.com/Soung2279/Mirai-Bot-Setup)为基础进行搭建，同时搭载了公主连结会战功能及日常娱乐功能

**感谢[Go-cqhttp](https://github.com/Mrs4s/go-cqhttp)项目，[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)项目，[Yobot](https://github.com/pcrbot/yobot)项目和众多[bot插件](https://www.pcrbot.com/) 的开发者们以及编写[Mirai-Bot部署指南](https://github.com/Soung2279/Mirai-Bot-Setup)的[@Soung2279](https://github.com/Soung2279)！**


**更新于2021年10月4日**

更新了资源包下载链接，现已包含全部所需图片/音频资源

## 目录
* [功能介绍](#功能介绍)
* [部署方法](#部署方法)
    * [准备工作](#准备工作)
    * [部署步骤](#部署步骤)
    * [开始使用](#开始使用)
    * [更进一步](#更进一步)
* [常见问题](#常见问题)
* [鸣谢](#鸣谢)

## 功能介绍
[详细功能列表](https://github.com/RMYHY/RBot/blob/main/HELP.md)

本机器人搭载了[Yobot 公主连结会战基本功能](http://yobot.win/features/)以及以下模块：
```python
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
    #'chachengfen',     #查成分B站关注列表
    'check',            #服务器状态查询
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
    'upguess',          #猜up（vtb/vup头像）
    'voiceguess',       #猜语音
    'weather',          #天气
    'whattoeat',        #今天吃什么
    #'wordcloud',       #词云
}
```
Bot 的功能繁多，可根据自身需要控制开关，在群聊中发送 `lssv` 即可查看各功能模块的启用状态，使用以下命令进行控制：

```
启用 service-name
禁用 service-name
```
为防止单条消息过长，每项功能的指令说明分别显示。使用以下命令可以查看各项功能的说明：

```
service-name帮助
```


## 部署方法

**本指南对[Mirai-Bot部署指南](https://github.com/Soung2279/Mirai-Bot-Setup)中的失效部分进行更新，再次感谢[@Soung2279](https://github.com/Soung2279)提供的入门级教程！**


### 准备工作

**本指南面向无编程基础或刚入门的萌新，故推荐使用具有图形界面，对新手操作友好的Windows服务器来进行部署**

- 准备一台Windows系统的服务器（或个人本地电脑）

- 准备一个作为bot的QQ小号 **（推荐绑定手机并开启设备锁以避免被腾讯风控）**

- 登录服务器控制台，在防火墙/安全组等界面，放通**80，8080，8090，9222**端口
> 以腾讯云为例：  
  在 云服务器 - 安全组 - 安全组规则 里 添加 入站与出站规则

> 以阿里云为例：  
  在 云服务器 - 防火墙 里 添加规则

> 以本地个人电脑为例：  
  在 控制面板 - 系统和安全 - Windows Defender 防火墙 - 高级设置 里 添加 入站规则 与 出站规则  
  不建议运行在本地个人电脑上。

- 在任意位置打开任意一个文件夹，点击左上方的`查看`-`显示/隐藏`页面中，勾选`文件扩展名`

### 部署步骤

1. 安装下列软件/工具

    - Python ：https://www.python.org/downloads/windows/
    - Git ：https://git-scm.com/download/win
    - Java ：https://www.java.com/zh_CN/download/win10.jsp
    - Notepad++ ：https://notepad-plus-plus.org/downloads/


2. 在合适的文件目录（例如桌面）新建文件夹并双击打开，点击文件夹左上角的 `文件 -> 打开Windows Powershell`，输入以下命令

    ```powershell
    git clone https://github.com/RMYHY/RBot.git
    ```

     或者直接下载本分支文件[RBot-main.zip](https://github.com/RMYHY/RBot.git)


3. 在合适的文件目录（推荐C盘根目录）新建文件夹并重命名为`Resources`  
    将收集到的 图片/语音资源 放入该文件夹，注意文件目录结构
    ```
    应当具有以下路径
    C:\Resources
    C:\Resources\img        总的图片存放位置
    C:\Resources\img\priconne       PCR实用小功能的图片位置
    C:\Resources\img\priconne\comic     PCR实用小功能-4格漫画
    C:\Resources\img\priconne\unit      PCR实用小功能-角色头像
    C:\Resources\img\priconne\quick     PCR实用小功能-rank表
    C:\Resources\img\setu       涩图
    C:\Resources\gacha      抽卡音效
    C:\Resources\MEGUMIN\explosion      爆裂魔法
    C:\Resources\pcrwarn        定时提醒语音
    ......
    ```
    **推荐**使用打包好的资源包,该资源包已包含RBot运行所需的所有图片/音频资源，下载后解压至C盘即可
    > 百度网盘：**[RBot资源包-Resources.zip(1.67GB)](https://pan.baidu.com/s/1huAfdEH_UK2lEcCdwrzkqw)**
    > 提取码：***4396*** 


4. 运行一次`yobot.exe`, 待弹出的窗口显示完毕后(*显示CTRL + C to quit字样后*)，关闭窗口


5. **修改以下几个文件的配置**

    - 在`yobot_data/yobot_config.json`文件中，将文中这几行语句内容更改为下列示例给出的内容（其他行不用改动，若和示例相同则无须变动。）
    ```json
    {
        "host": "0.0.0.0",
        "port": 9222,
        "public_address": "http://你的服务器公网IP:9222/",
    }
    ```

    - 在`config.yml`文件中，用需要**作为bot的QQ号**替换`uin`之后的数字
    **推荐不填密码使用扫码登录**（使用密码登录会触发较难处理的滑块验证）
    ```yml
    account: # 账号相关
      uin: 3385546539 # QQ账号
      password: '' # 密码为空时使用扫码登录
    ```

    - 在`HoshinoBot/hoshino/config/_bot_.py`文件中，将`SUPERUSERS`后的数字改为**你自己的QQ号**，将NICKNAME后的名称更改为**你自定义的名字**，将`RES_DIR`后的路径改为你在**第三步**新建的`Resources`路径
    ```python
    SUPERUSERS = [549883020,1061301935] # 填写超级用户的QQ号，可填多个用半角逗号","隔开
    NICKNAME = 'bot', 'hina', '氷川日菜' # 机器人的昵称。呼叫昵称等同于@bot，可用元组配置多个昵称
    RES_DIR = r'C:/Resources/' # 资源路径
    ```

6. 在`RBot\HoshinoBot`目录下点击文件夹左上角的 `文件 -> 打开Windows Powershell`，输入以下命令
    ```python
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
    ```
    或者直接运行`双击安装依赖.bat`，若此过程中有报错信息，请重新运行一次，若仍有报错，请复制报错信息到搜索引擎获得帮助

7. (可选) 在以下文件中填入你自己的APIKEY
   - 在`HoshinoBot/hoshino/config/priconne.py`文件里添加[竞技场作业网](https://pcrdfans.com/)的API（目前已无法[申请](https://pcrdfans.com/bot)，建议需要此功能的群友手动登陆网站查询）
   ```python
   class arena:
    AUTH_KEY = "你的作业网API"
   ```

   - 在`HoshinoBot/hoshino/modules/search-image/picfinder.py`文件里**第15行**添加[SauceNAO识别图片](https://saucenao.com/index.php)的API（需要去[申请](https://saucenao.com/user.php)，已内置了我自己的API，但过多使用可能造成请求额度不够）
   ```python
    api_key="abcdefghijklmn123"#填写你自己的api_key
   ```

### 开始使用
运行 `RBot` 下的 `yobot.exe` , `go-cqhttp.exe` 和 `HoshinoBot` 下的 `双击运行HoshinoBot.bat`。

显示以下字样说明bot启动成功：
#### *双击运行HoshinoBot.bat*
```powershell
Running on http://127.0.0.1:8090 (CTRL + C to quit)
```

#### *yobot.exe*
```powershell
yobot[v3.6.12]便携版
初始化完成，启动服务...
Running on https://0.0.0.0:9222 (CTRL + C to quit)
```
#### *go-cqhttp.exe*
```powershell
[INFO]: 登录成功 欢迎使用: QQ昵称
[INFO]: 开始加载好友列表...
[INFO]: 共加载 N 个好友.
[INFO]: 开始加载群列表...
[INFO]: 共加载 N 个群.
[INFO]: 收到服务器地址更新通知, 将在下一次重连时应用.
[INFO]: 信息数据库初始化完成.
[INFO]: 正在加载事件过滤器.
[INFO]: 资源初始化完成, 开始处理信息.
[INFO]: 开始尝试连接到反向WebSocket Universal服务器: ws://127.0.0.1:9222/ws/
[INFO]: 开始尝试连接到反向WebSocket Universal服务器: ws://127.0.0.1:8090/ws/
[INFO]: アトリは、高性能ですから!
[INFO]: 正在检查更新.
[INFO]: 检查更新完成. 当前已运行最新版本.
```

> go-cqhttp.exe第一次运行需用手机登录**作为bot的QQ号**扫码验证，若使用密码登录遇到[滑块验证码请参阅官方文档](https://docs.go-cqhttp.org/faq/slider.html)

> HoshinoBot初始化过程中常见的报错为资源缺失，请确认**第五步**中修改的`RES_DIR`路径是否正确

> 若HoshinoBot初始化过程中出现类似报错信息：
> ERROR: Failed to import "xxx", error: No module named 'abc'
> ERROR: No module named 'abc'
> 说明 abc 依赖项未安装，请在任意文件夹点击文件夹左上角的 `文件 -> 打开Windows Powershell`，输入以下命令
> pip install abc

在bot所在群聊中发送任意信息，若`go-cqhttp.exe` 和 `双击运行HoshinoBot.bat`窗口**有反应**，说明bot的HoshinoBot部分**正常**运行中。此时请发送`lssv`来确认当前群启用的服务，也可以发送【使用指南】/【指令表】来查看bot的帮助文档。  

在bot所在群聊中发送`version`和`help`，若bot在群聊中有反应，说明bot的Yobot部分**正常**运行中。此时可发送【help】来查看bot的会战文档，或私聊bot发送【登录】启用Yobot的Web面板。

### 更进一步
- 若Bot 运行正常，可考虑开启更多模块以丰富bot的功能。

- 在 `HoshinoBot/hoshino/config/_bot_.py` 文件里，将需要开启的模块前面的"`#井号`"删除。

- 若想给Bot 添加更多功能，可以自行收集插件放入 `HoshinoBot/hoshino/modules` 文件夹中。（请仔细阅读该插件的说明文档，某些插件的添加方式有所不同）

- 若Bot 添加群过多，需要引入授权系统，请启用[authMS](https://github.com/pcrbot/authMS)插件。Bot 已内置此插件，请仔细阅读说明文档进行配置。

- 可自定义的内容
    - `modules/botchat/botchat.py`：这是**bot的轻量语言库**，可自行添加语句和回复，源文件里已包含范例。不同bot的人格差异化也基于此体现。

    - `modules/explosion/exo.py`：这是**爆裂魔法**，可自行更改日调用上限，也可以自行魔改添加更多语音。

    - `modules/generator-image/`：这是**表情包生成器**，可在`meme`里自行添加更多表情包。

    - `modules/HELP`：这是Bot 的**帮助文档**，可自行更改文本内容。

    - `hoshino/config/hourcall.py`：这是**整点时报**的文本内容，可自行更改，也可自行仿照格式添加。

    - `modules/pcrwarn`：这是**定时提醒**，可自行更改提醒时间，提醒内容。

    - `modules/priconne/gacha/`：这是**模拟抽卡**，可在`gacha.py`中自行更改抽卡次数日上限，还可在`config.json`中自行更改卡池内容。

    - `modules/setu/setu.py`：这是**涩图**，可自行更改日调用上限。

    - `modules/hiumsentences/`：这是**随机网抑云**，可在`nt_words.json`中自行更改语录文本。

**参考[HoshinoBot(v2) 插件开发指南（社区版）](https://github.com/pcrbot/hoshinobot-development-documentation)**

## 常见问题  

- 为什么我的Bot 发不出图片/语音？
    - 请检查资源路径`RES_DIR`是否设置正确，目录`Resources`下该图片/语音是否存在  

- 为什么我的Bot 没有反应？
    - 请查看窗口显示的日志。  
    - 若日志显示正常，请查看在[**准备工作**](#准备工作)步骤中是否放通端口。
    - 若`go-cqhttp.exe`显示 **“群消息发送失败，账号可能被风控”**，请关闭go-cqhttp并删除RBot文件夹的`device.json`及`session.token`文件，再打开go-cqhttp重新登录 **（推荐作为bot的QQ账号绑定手机并开启设备锁以避免被腾讯风控）**
    - 若日志有报错信息，请复制报错信息到搜索引擎解决。
    - 若日志无反应，请在该窗口输入回车`(按下Enter键)`，查看日志是否有反应。若日志仍无反应，请查看在[**部署步骤 - 5.修改以下几个文件的配置**](#部署步骤)中的文件是否正确配置
    - 若端口已经放通，请尝试其它指令；若部分指令有回应，说明bot 正常运行中，只是部分消息被tx吞了。若所有指令都无回应，请重新运行`双击安装依赖`
    - 若所有方式都无法让Bot 做出反应，请尝试重新部署Bot。

- Bot 的权限是怎么设定的？
    - A：基于HoshinoBot的功能，设定主人为**最高**权限`priv.SUPERUSER`，群主为仅次于主人的第二权限`priv.OWNER`，群管理为更次一等的权限`priv.ADMIN`，群员为最低权限`priv.NORMAL`。(黑/白名单不考虑在内) 主人可以在`_bot_.py`里设定多个 
    - A：而基于Yobot的功能，需要在面板中单独设定群员`公会战管理员`和`成员`，默认群员为`成员`，`公会战管理员`可以设置**多个**，但`主人`只能设定**一个**

- 以后的更新维护？
    - 您可以自行访问[Go-cqhttp](https://github.com/Mrs4s/go-cqhttp)项目，[HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)项目，[Yobot](https://github.com/pcrbot/yobot)项目和众多[bot插件](https://www.pcrbot.com/)来进行更新。

- 还有什么注意事项？
    - 请勿滥用Bot。

## 鸣谢

### 骨干部分

**HoshinoBot**：https://github.com/Ice-Cirno/HoshinoBot  作者：[@Ice-Cirno](https://github.com/Ice-Cirno)

**Yobot**：http://yobot.win/  作者：[@yuudi](https://github.com/yuudi)

**go-cqhttp**：https://github.com/Mrs4s/go-cqhttp  作者：[@Mrs4s](https://github.com/Mrs4s/)

**Mirai-Bot-Setup**：https://github.com/Soung2279/Mirai-Bot-Setup  作者：[@Soung2279](https://github.com/Soung2279/)

### 插件部分

- [**Dihe Chen**](https://github.com/Chendihe4975)  
- [**var**](https://github.com/var-mixer)  
- [**xhl6699**](https://github.com/xhl6666)  
- [**Watanabe-Asa**](https://github.com/Watanabe-Asa)  
- [**-LAN-**](https://github.com/laipz8200)  
- [**Cappuccilo**](https://github.com/Cappuccilo)  
- [**yuyumoko**](https://github.com/yuyumoko)  
- [**H-K-Y**](https://github.com/H-K-Y)  
- [**ZhouYuan**](https://github.com/zyujs) 
- [**sdyxxjj123**](https://github.com/sdyxxjj123) 
- [**Rs794613**](https://github.com/Rs794613)  
...

### 资源部分

**干炸里脊资源站**: https://redive.estertion.win/

**Pcrbot - pcrbot相关仓库**: https://www.pcrbot.com/

###   本项目基于[GNU通用公共授权3.0](http://www.gnu.org/licenses/) 开源



