# Asill
## A-soul 发病小作文
真情实感发病小作文选自[枝江作文展](https://asoulcnki.asia/rank)

### 安装
将 `data.json` 与 `asill.py` 至于同一个文件夹并放在 `HoshinoBot/hoshino/modules` 目录下

修改 `HoshinoBot/hoshino/config/__bot__.py` 文件，在 `MODULES_ON = {}` 配置中添加`'asill'`
```python
# 启用的模块
MODULES_ON = {
    ...
    'asill',
    ...
}
```

### 使用指南
| 指令 | 说明 |
| --- | --- |
|发病 对象|	发送一篇写给对象的发病小作文
|小作文|	随机发送一篇库存发病小作文
|病情加重 对象/小作文|	将一篇发病小作文添加到数据库中

添加小作文时对象为小作文中对方的称呼（暂不支持多称呼）且斜杠“/”不可省略

在群聊中添加小作文可能导致json文件预览无法显示汉字（实际功能正常）建议直接修改原文件

### 修改作文
修改`data.json`可自定义修改小作文
```json
[
    {
        "person":"发病对象1",
        "text":"小作文内容1"
    },
    {
        "person":"发病对象2",
        "text":"小作文内容2"
    }, 
    ...
    ...
    {
        "person":"发病对象n",
        "text":"小作文内容n"
    }
]
```
