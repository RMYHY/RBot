# hoshinobot-plugin-ddcheck

Hoshinobot 成分姬插件

查询B站关注列表的VTuber成分，并以图片形式发出

插件移植自[nonebot-plugin-ddcheck](https://github.com/noneplugin/nonebot-plugin-ddcheck)

VTB列表数据来源：[vtbs.moe](https://vtbs.moe/)


### 使用方式

**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行在bot.py中的COMMAND_START设置为空**

```
查成分 + B站用户名/UID
```


### 安装

```
git clone https://github.com/benx1n/hoshinobot-plugin-ddcheck.git

pip install -r requirements.txt

将config_example.json重命名为config.json

在bot.py中添加'hoshinobot-plugin-ddcheck'
```

若要显示主播牌子，需要在 `.config.json` 文件中添加任意的B站用户cookie：

```
"cookie" = "xxx"
```


### 示例

<div align="left">
  <img src="https://s2.loli.net/2022/03/20/Nk3jZJgxforHDsu.png" width="400" />
</div>
