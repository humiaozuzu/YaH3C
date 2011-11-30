YaH3C
=====

YaH3C is a H3c authentication client for SYSU east campus.

Dependencies
------------

* Linux Platform
* Python2 (Python3 is not supported)

Installation
------------

use the following bash scripts to install:

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

ScreenShots
----------

Authenticate successfully:
![success](https://github.com/humiaozuzu/YaH3C/blob/master/screenshots/success.png?raw=true)

Authenticate failed:
![failure](https://github.com/humiaozuzu/YaH3C/raw/master/screenshots/failure.png)


Todo
----
* Windows platform support
* Command line argument support
* Multiuser management
* Web UI

Thanks
------
* [qiao](https://github.com/qiao) - Write python installation script for YaH3C
* [houqp](https://github.com/houqp) - Refered to houqp's [pyh3c](https://github.com/houqp/pyh3c).
