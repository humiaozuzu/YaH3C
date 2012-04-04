YaH3C
=====

YaH3C 是用于校园网认证的客户端，支持中山大学东校区.

依赖
------------

* Linux
* Python2 (Python3暂不支持)

安装
------------

首先从github上下载，可以直接利用`git clone`，也可以下载压缩包自己解压然后安装。下面以git为例，如果没有则需要先安装：

```bash
# Ubuntu/Debian
sudo apt-get install git

# ArchLinux
sudo pacman -S git
```
然后从项目中clone下来并安装

```bash
git clone git://github.com/humiaozuzu/YaH3C.git
cd YaH3C
make
sudo make install
```

**ArchLinux**默认安装的python是python3，你需要手动安装python2。

使用
----

### 认证

程序运行时必须要有root权限：

```bash
sudo yah3c
```

然后根据程序的提示输入账号密码就可以开始认证了。

### 联网

因为YaH3C仅仅是**认证**客户端，所以通过认证后你需要自己联网，一般学校都是使用的dhcp协议获取ip。

你可以通过你自己喜欢的方式获取ip，命令行的或者是NetworkManager/Wicd：

```bash
# 以dhcpcd为例
sudo dhcpcd eth0
```

配置文件
--------

所有用户的登陆信息和配置文件都放在`~/.yah3c/`目录下，可以自己根据需求进行修改。

    ~/yah3c/
    ├── plugins            # 插件目录
    │   ├── auto_dhcp.py
    │   ├── __init__.py
    │   ├── notify.py
    │   ├── plugin_template.py
    │   └── test.py
    └── users.conf         # 保存用户的登陆信息

用户的登陆信息按照如下的格式保存在文件`users.conf`中：

```
[account]          # 你的帐户 
password = 123456  # 密码
dev = eth0         # 使用的网卡
```

插件
----

目前插件机制还不是很完善，默认是没有启用任何插件的。

### plugins::notify ###

调用`python-notify`提示用户在线或掉线。

KDE的用户可能回遇到下面错误或者notify不显示的情况：

```bash
No protocol specified\nAutolaunch error: X11 initialization failed.\n
```

有2种解决方案：

 1. 在终端执行`xhost +local:root`，或讲其添加到`.bash_profile`一劳永逸解决问题。
 2. 执行`visudo`后添加下面的配置 

 ```bash
Defaults env_keep += "HOME"
```

### plugins::auto_dhcp ###

这个插件会在你登陆成功后使用dhcpcd帮你自动获取ip。

### 为YaH3C贡献插件

你可以参考``~/.yah3c/plugins/plugin_template.py``文件，了解如何为YaH3C编写插件，更详细的信息可以参考[wiki](https://github.com/humiaozuzu/YaH3C/wiki/4.-YaH3C插件机制)

ScreenShots
-----------

认证成功:

![success](https://github.com/humiaozuzu/YaH3C/blob/master/screenshots/success.png?raw=true)

认证失败:

![failure](https://github.com/humiaozuzu/YaH3C/raw/master/screenshots/failure.png)

Updates
-------

Ver 0.3

* add eap-md5 support

Ver 0.2

* complete refactory 
* plugins support

Ver 0.01

* Initial commit

Todo
----
* Command line argument support
* Web UI
* Tray icon

Thanks
------
* [qiao](https://github.com/qiao) - Write python installation script for YaH3C.
* [houqp](https://github.com/houqp) - Refered to houqp's [pyh3c](https://github.com/houqp/pyh3c).
* [tigersoldier](https://github.com/tigersoldier) - Write EAP-Md5 for YaH3C.
