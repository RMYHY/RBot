# pcr_calendar

公主连结图形化活动日历插件, 适用于 `HoshinoBot v2`.

项目地址 <https://github.com/zyujs/pcr_calendar>

![calendar](https://user-images.githubusercontent.com/3376669/104091785-b476a080-52ba-11eb-9d0a-763cb29cc9b6.png)

## 日程信息源

- 国服: [MahoMaho INSIGHT!! 真步真步视界术](https://mahomaho-insight.info/)
- 台服: [蘭德索爾圖書館](https://pcredivewiki.tw/)
- 日服: [https://tools.yobot.win/](https://tools.yobot.win/calender/#jp)

## 安装方法

1. 在HoshinoBot的插件目录modules下clone本项目 `git clone https://github.com/zyujs/pcr_calendar.git`
1. 在 `config/__bot__.py`的模块列表里加入 `pcr_calendar`
1. 重启HoshinoBot

## 指令列表

- `日历` : 查看本群订阅服务器日历
- `[国台日]服日历` : 查看指定服务器日程
- `[国台日]服日历 on/off` : 订阅/取消订阅指定服务器的日历推送
- `日历 time 时:分` : 设置日历推送时间
- `日历 status` : 查看本群日历推送设置
- `日历 cardimage` : (go-cqhttp限定)切换是否使用cardimage模式发送日历图片
