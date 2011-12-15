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
make
sudo make install
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
# dhcpcd as an example 
$ sudo dhcpcd eth0
```

Resource files
-------------

All users logging info and plugins are stored in the folder **~/.yah3c/**

    ~/yah3c/
    ├── plugins            # plugins folder
    │   ├── auto_dhcp.py
    │   ├── __init__.py
    │   ├── notify.py
    │   ├── plugin_template.py
    │   └── test.py
    └── users.conf         # storing all users' logging info 

A user's logging info is organized in the following format in **users.conf**:

```
    [account]          # your net ID
    password = 123456  # password for your net ID
    dev = eth0         # Ethernet card you use for authentication
```

You can refer to **~/.yah3c/plugins/plugin_template.py** to known how to write
a plugin for YaH3C.


### notify ###

This plugin will use `python-notify` to indicate the user when he is
online/offline.

You may meet with following error message when logging in, and the notify won't
show up:

```bash
No protocol specified\nAutolaunch error: X11 initialization failed.\n
```

There are both ways to solve the problem:

 1. excute `xhost +local:root` or add it to your `.bash_profile` once and for
 all.
 2. Add the following line to `sudoers` file(using `visudo`): 

 ```bash
Defaults env_keep += "HOME"
```

### auto_dhcp ###
This plugin will use `dhcpcd` to allocate for ip adress  after you have
successfully logged in.


ScreenShots
-----------

Authenticate successfully:

![success](https://github.com/humiaozuzu/YaH3C/blob/master/screenshots/success.png?raw=true)

Authenticate failed:

![failure](https://github.com/humiaozuzu/YaH3C/raw/master/screenshots/failure.png)

Updates
-------

Ver 0.2

* complete refactory 
* plugins support

Ver 0.01

* Initial commit

Todo
----
* Windows platform support
* Command line argument support
* Web UI

Thanks
------
* [qiao](https://github.com/qiao) - Write python installation script for YaH3C
* [houqp](https://github.com/houqp) - Refered to houqp's [pyh3c](https://github.com/houqp/pyh3c).
