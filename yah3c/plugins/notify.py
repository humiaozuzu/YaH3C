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
