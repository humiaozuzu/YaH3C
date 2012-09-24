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
sudo python setup.py
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

因为YaH3C仅仅是**认证**客户端，所以通过认证后你需要自己联网，不过为了方便还是添加了dhcp支持。

如果没有指定dhcp的命令，你可以在认证成功后使用自己喜欢的网络管理工具获取IP，如NetworkManager/Wicd。

yah3c支持基本的命令行参数，执行`yah3c -h`可以看到支持的命令行参数

``` bash
$ yah3c -h       
usage: yah3c [-h] [-u USERNAME] [-debug]

Yet Another H3C Authentication Client

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Login in with this username
  -debug                Enable debugging mode
```

如执行`sudo yah3c -u Maple`可以自动认证`Maple`这个帐号

配置文件格式
---------
用户的登陆信息按照如下的格式保存在文件`/etc/yah3c.conf`中：

``` ini
[account]                  # 你的帐户 
password = 123456          # 密码
ethernet_interface = eth0  # 使用的网卡
dhcp_command =             # 验证成功后使用的dhcp命令
daemon = True              # 验证成功后是否变成daemon进程
```

ScreenShots
-----------

认证成功:

![success](https://github.com/humiaozuzu/YaH3C/blob/master/screenshots/success.png?raw=true)

认证失败:

![failure](https://github.com/humiaozuzu/YaH3C/raw/master/screenshots/failure.png)


Todo
----
* BSD BPF support

Thanks
------
* [qiao](https://github.com/qiao) - Write python installation script for YaH3C.
* [houqp](https://github.com/houqp) - Refered to houqp's [pyh3c](https://github.com/houqp/pyh3c).
* [tigersoldier](https://github.com/tigersoldier) - Write EAP-Md5 for YaH3C.
