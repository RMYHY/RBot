# 群聊输出二维码

---
这是 Hoshino 的插件</br>

安装依赖
> pip install pyzbar -i https://pypi.tuna.tsinghua.edu.cn/simple


---

## 识别到二维码后直接发送链接

### (你们发二维码能不能照顾一下PC端啊)

<br>

### 如果你发现以下报错
![image](./doc/error.png)

那你可能需要安装[Visual C++ Redistributable Packages for Visual Studio 2013](https://www.microsoft.com/zh-CN/download/details.aspx?id=40784)

### 如果你是centos只pip3 install pyzbar的话会报错 (by @SlightDust #1)
需要`yum install zbar-devel`一下即可
