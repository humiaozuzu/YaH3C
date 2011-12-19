import commands
import sys
from time import sleep

root_privilege = True

dhcp_client = 'dhcpcd'
dhcp_args = ''

def before_auth(yah3c_info):
    pass

def after_auth_fail(yah3c_info):
    pass

def after_auth_succ(yah3c_info):
    #remain_sec = 3
    #for 
    #sys.stdout.write('\r')
    #sys.stdout.flush()
    print 'use', dhcp_client, 'to obtain ip address'
    print commands.getoutput('dhcpcd eth0')

def after_logoff(yah3c_info):
    pass
