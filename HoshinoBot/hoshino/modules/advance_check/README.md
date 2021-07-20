# Advance_check_hoshinobot
***
## bot服务器配置查询

**默认文件夹名：advance_check**
**默认服务名：advance_check**
**目录组成如下：**

> **advance_check**
>> advance_check.py  #主要运行文件
>> requirements.txt  #依赖说明
>> README.md  #说明文件

### 功能介绍

利用 python库-[WMI](https://pypi.org/project/WMI/) 查询电脑硬件配置相关信息。

~~人称小鲁大师~~

可以查询的信息有如下：
- 获取**电脑使用者**信息
- 获取**操作系统**信息
- 获取**电脑IP和MAC**信息
- 获取**电脑CPU**信息
- 获取**BIOS**信息
- 获取**磁盘**信息
- 获取**显卡**信息
- 获取**内存**信息
- ……


需要 **@bot** 使用，当然你也可以自己改成无需@。在 **advance_check.py** 文件里我做了详细的注释，小白也能看懂

### 安装

#### 通过github克隆

在hoshino/modules文件夹中，打开cmd或者powershell，输入以下代码按回车执行：
```powershell
git clone https://github.com/Soung2279/advance_check_hoshinobot.git
```
之后不要关闭cmd或powershell，输入以下代码安装依赖
```powershell
py -3.8 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```
之后关闭cmd或powershell，在hoshino/config的`__bot__.py`文件中，在MODULES_ON = {}里添加advance_check
```python
# 启用的模块
MODULES_ON = {
    'xxx',
    'xxx',
    'advance_check',  #注意英文逗号！
    'xxx',
    'xxx',
}
```

#### 直接安装

直接下载本文件夹（advance_check），将其放入hoshino/modules中，并安装依赖[WMI](https://pypi.org/project/WMI/)
提供如下安装依赖代码，可直接复制到cmd/powershell当中，按回车执行。
```powershell
py -3.8 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```
之后关闭cmd或powershell，在hoshino/config的`__bot__.py`文件中，在MODULES_ON = {}里添加advance_check
```python
# 启用的模块
MODULES_ON = {
    'xxx',
    'xxx',
    'advance_check',  #注意英文逗号！
    'xxx',
    'xxx',
}
```

### 指令

- **`[@bot adcheck/鲁大师/看看配置/看看服务器/adck]`** 看看服务器硬件配置
- **`[帮助advance_check]`** 查看详情

### 可自定义内容

在 **[advance_check.py](https://github.com/Soung2279/advance_check_hoshinobot/advance_check.py)** 文件的第 **19-23** 行可自行设置是否启用**合并转发**和**定时撤回**功能

```python
forward_msg_exchange = 1  #是否启用合并转发。1是启用，0是禁用
forward_msg_name = '在这里输入合并转发的呢称'  #转发用的昵称
forward_msg_uid = '756160433'  #转发用的UID，懒得想或者要用官方的UID可以参考下面
recall_msg_set = 1  #是否启用定时撤回。1是启用，0是禁用
RECALL_MSG_TIME = 30  #撤回前的时长，单位s
```

>还有一些其它的可以自己改的我都写在文件注释里面了。根据注释说明自己改吧~（保持原样也可以使用！）

### 其它

本人非专业程序员，业余写着玩玩，代码很菜，大佬们看看就好QwQ。

made by [Soung2279@Github](https://github.com/Soung2279/)

### 鸣谢

灵感来源：自检[check](https://github.com/pcrbot/Hoshino-plugin-transplant#%E8%87%AA%E6%A3%80)  作者 **[Watanabe-Asa](https://github.com/Watanabe-Asa?tab=repositories)**
