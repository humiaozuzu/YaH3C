# ===============================================================
#
# This is a plugin template, we have 3 hooks in YaH3C:
# 
#  * before_auth() will be called just before sending start authentication packet.
#
#  * after_auth_succ() will be called after received authentication succed packet.
#
#  * after_auth_fail() will be called after received authentication failed packet.
# 
#  * after_logoff() will be called after you logoff
#
# ===============================================================
#
# Here are some attributes that you may want to use in your functions:
#  pyh3c.h3cStatus: 
#    A h3cStatus instance 
#
#  pyh3c.plugins_loaded: 
#    A list containning objects for loaded plugins.
#
#  pyh3c.lock_file:
#    A string, path for lock file
#
#  pyh3c.h3cStatus.dev:
#    String, name for selected network interface 
#
#  pyh3c.h3cStatus.hwadd:
#    String, hardware address for pyh3c.h3cStatus.dev.
#
#  pyh3c.h3cStatus.user_name:
#    String, user name of the account
#
#  pyh3c.h3cStatus.user_pass:
#    String, user pass of the account
#
#  pyh3c.h3cStatus.dhcp_command:
#    String, command used to acquire dynamic ip
#
#  pyh3c.h3cStatus.plugins_to_load:
#    List of string, each string is the name for plugins 
#    that user want to load. Its content is initialized 
#    according to pyh3c.conf, more specifically, according 
#    to plugins option in sys_conf section.
#
#  pyh3c.h3cStatus.ping_target:
#    String, can be ip address or domain. Should be 
#    self-explanatory.
#
#  pyh3c.h3cStatus.ping_interval:
#    Int, time interval between each ping action, in seconds
#
#  pyh3c.h3cStatus.ping_tolerence:
#    Int, maxium ping failed time. When exceed this value,
#    authentication start packet will be resent.
#
#  pyh3c.h3cStatus.auth_success:
#    Int, 1 for successful authentication, 0 for not 
#    yet authenticated.
#
#  pyh3c.h3cStatus.parser:
#    A SafeConfigParser instance, used to manipulate 
#    configuration.

import os

root_privilege = False

try:
    import pynotify
except ImportError:
    print 'Please install package python-notify'

pynotify.init ("YaH3C")

def before_auth(yah3c_info):
    pass

def after_auth_succ(yah3c_info):
    msg = pynotify.Notification('YaH3C', "Authenticate Successfully!")
    msg.show()

def after_auth_fail(yah3c_info):
    msg = pynotify.Notification('YaH3C', "Authenticate Failed!")
    msg.show()

def after_logoff(yah3c_info):
    msg = pynotify.Notification('YaH3C', "Logoff Successfully!")
    msg.show()
