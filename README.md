YaH3C
=====

YaH3C 是用于校园网认证的客户端，支持中山大学东校区。

感谢 [lpy](https://github.com/lpy) 为 OS X 提供的[版本](https://github.com/lpy/Yah3c)。

为什么不用iNode
---------------

* i开头完全是对Apple的侮辱嘛 = =
* 强制添加启动项
* gui和cli使用的udp交互，很多时候Linux/Mac下掉线完全是因为实现的效率太低
* 安装脚本居然是自删除的
* 默认强制记录日志文件，增加CPU负载，减少硬盘寿命，一段时间后就过GB了（是否有敏感信息不得而知了）
* Linux下仅仅支持Ubuntu 32位系统
* Mac下安装后居然要重启
* 使用的第三方库乱放和HomeBrew冲突

依赖
------------
 
* 主流Linux发行版，包括OpenWrt/DD-WRT
* Python2

安装
------------

首先，从github上下载，可以直接利用`git clone`，也可以下载压缩包自己解压然后安装。下面以git为例，如果没有则需要先安装：

```bash
# Ubuntu/Debian
sudo apt-get install git

# ArchLinux
sudo pacman -S git
```
然后，从项目中clone下来并安装

```bash
git clone git://github.com/humiaozuzu/YaH3C.git
cd YaH3C
sudo python setup.py install
```

**ArchLinux**默认安装的python是python3，你需要手动安装python2。

使用
----

完整的联网过程有2步，首先使用本客户端通过交换机的认证，然后获取ip。

### 认证

程序运行时必须要有root权限：

```bash
sudo yah3c
```

根据程序的提示输入账号密码就可以开始认证了，有些选项如果看不懂请直接按`Enter`。

### 获取ip

因为YaH3C仅仅是**认证**客户端，所以通过认证后你需要自己获取ip联网，不过为了方便还是添加了dhcp支持。

如果没有指定dhcp的命令，你可以在认证成功后使用自己喜欢的网络管理工具获取IP，如NetworkManager或Wicd。

YaH3C支持基本的命令行参数，执行`yah3c -h`可以看到支持的命令行参数

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
ethernet_interface = eth0  # 使用的网卡，默认为eth0
dhcp_command = dhcpcd      # 验证成功后使用的dhcp命令(dhcpcd/dhclient)，默认为空
daemon = True              # 验证成功后是否变成daemon进程，默认为是
```

ScreenShots
-----------

认证成功:

![success](https://raw.github.com/humiaozuzu/YaH3C/master/screenshots/success.png)

认证失败:

![failure](https://raw.github.com/humiaozuzu/YaH3C/master/screenshots/failure.png)


Todo
----
* ~~添加BSD BPF 支持，这样在OS X也可以使用了~~
* 完善收集调试信息的功能，方便用户提交认证信息
* 完善对H3C协议的支持

Thanks
------
* [qiao](https://github.com/qiao) - Write python installation script for YaH3C
* [houqp](https://github.com/houqp) - Refered to houqp's [pyh3c](https://github.com/houqp/pyh3c)
* [tigersoldier](https://github.com/tigersoldier) - Write EAP-Md5 for YaH3C

License
-------
YaH3C的代码使用MIT License发布，此外，禁止使用YaH3C以及YaH3C的修改程序用于商业目的（比如交叉编译到路由进行销售等行为）
