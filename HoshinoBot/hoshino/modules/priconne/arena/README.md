# jjc查询图片版
本模块由[ellye](https://github.com/watermellye)完善功能，增加截图查询功能

支持全屏和部分截图；当截图中含有多队时返回无冲配队。

## 食用方法

用本repo将hoshino/modules/priconne/arena替换即可。

## 指令

b/日/台jjc + 防守队伍文字/防守队伍截图 （无须+号）

## 注意

由于api存在次数和频率限制，请勿出于好奇进行过多尝试。

dic.npy其实为hoshino/res/img/priconne/unit中的pcr图像，读取成numpy数组后的打包保存文件。因此其不支持日服最新角色。若有相关需求，请使用文字查询。

## 使用例

### pjjc
![pjjc1](images/pjjc1.png)


![pjjc2](images/pjjc2.png)


![pjjc3](images/pjjc3.png)

### jjc
![jjc1](images/jjc1.png)


![jjc2](images/jjc2.png)

### 部分截图
![segment1](images/segment1.png)

### 其它
![other1](images/other1.png)


![other2](images/other2-16477551166681.png)


————以下为原README————

本模块基于 0皆无0（NGA uid=60429400）dalao的[PCR姬器人：可可萝·Android](https://bbs.nga.cn/read.php?tid=18434108)，移植至nonebot框架而成。

重构 by IceCoffee

源代码的使用已获原作者授权。
