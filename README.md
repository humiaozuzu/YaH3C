YaH3C
=====

YaH3C is a H3c authentication client for SYSU east campus.

Dependencies
------------

* Linux Platform
* Python2 (Python3 is not supported)

Installation
------------
You should have **git** installed first, if not:

```bash
# Ubuntui/Debian users
sudo apt-get install git

# ArchLinux users
sudo pacman -S git
```

Then use the following bash scripts to install:

```bash
git clone git://github.com/humiaozuzu/YaH3C.git
cd YaH3C
sudo python setup.py install
```

For **Arch** users, be sure to use **python2**

Usage
-----

You must run the program with root privilege:

```bash
$ sudo yah3c
```
Use dhcpcd/dhclients or other network management tools(NetworkManager/wicd) to obtain IP address

```bash
$ sudo dhcped eth0
```

ScreenShots
----------

Authenticate successfully:

![success](https://github.com/humiaozuzu/YaH3C/blob/master/screenshots/success.png?raw=true)

Authenticate failed:

![failure](https://github.com/humiaozuzu/YaH3C/raw/master/screenshots/failure.png)


Todo
----
* Windows platform support
* daemonize
* Command line argument support
* Multiuser management
* Web UI

Thanks
------
* [qiao](https://github.com/qiao) - Write python installation script for YaH3C
* [houqp](https://github.com/houqp) - Refered to houqp's [pyh3c](https://github.com/houqp/pyh3c).
