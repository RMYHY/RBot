## good_morning

一个适用hoshinobot的 早安晚安 插件

功能仿造自[BillYang2016](https://github.com/BillYang2016)的酷Q早安晚安插件，已获原作者授权

插件后续将继续在 github 不定期更新，欢迎提交 isuue 和 request

本插件仅供学习研究使用，插件免费，请勿用于违法商业用途，一切后果自己承担

## 项目地址：

https://github.com/azmiao/good_morning

## 更新日志

21-10-29    v1.2    修复一点点恶性bug，命令调设置再写了2333

21-10-25    v1.1    新增睡眠时长和清醒时长显示，新增性别显示，尽量还原酷Q版功能吧

21-10-23    v1.0    大概能用了？

## 功能

```
[早安晚安初始化] 初始化，限超级管理员
[早安] 早安喵
[晚安] 晚安喵
[我的作息] 看看自己的作息
[群友作息] 看看今天几个人睡觉或起床了
```

## 简单食用教程：

1. 下载或git clone本插件：

    在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目
    ```
    git clone https://github.com/azmiao/good_morning
    ```

2. 在 HoshinoBot\hoshino\config\ `__bot__.py` 文件的 MODULES_ON 加入 'good_morning'

    然后重启 HoshinoBot

3. 在群里发一句'早安晚安初始化'初始化一下

4. 一些功能可自由配置，且可以随时修改无需重启hoshino，具体配置内容见下文

## 功能配置

### 打开文件 `config.json`

```
{
    "morning": {
        "get_up_intime": {      //是否只能在规定时间起床床
            "enable": true,     //默认开启，若关闭则下面两项无效
            "early_time": 1,    //允许的最早的起床时间
            "late_time": 18     //允许的最晚的起床时间
        },
        "multi_get_up": {       //是否允许多次起床
            "enable": false,    //默认不允许，若开启则下面一项无效
            "interval": 6       //两次起床间隔的时间，小于这个时间就不允许起床
        },
        "super_get_up": {       //是否允许超级亢奋
            "enable": false,    //默认不允许，若开启则下面一项无效
            "interval": 3       //这次起床和上一次睡觉的时间间隔，小于这个时间就不允许起床，不怕猝死？给我睡！
        }
    },
    "night": {
        "sleep_intime": {       //是否只能在规定时间睡觉觉
            "enable": true,     //默认开启，若关闭则下面两项无效
            "early_time": 18,   //允许的最早的睡觉时间，默认晚上18点
            "late_time": 6      //允许的最晚的睡觉时间，默认第二天早上6点
        },
        "multi_sleep": {        //是否允许多次睡觉
            "enable": false,    //默认不允许，若开启则下面一项无效
            "interval": 6       //两次睡觉间隔的时间，小于这个时间就不允许睡觉
        },
        "super_sleep": {        //是否允许超级睡眠
            "enable": false,    //默认不允许，若开启则下面一项无效
            "interval": 3       //这次睡觉和上一次起床的时间间隔，小于这个时间就不允许睡觉，睡个锤子，快起床！
        }
    }
}
```