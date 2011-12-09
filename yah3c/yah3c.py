#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys
from socket import *
import ConfigParser
import getpass

from eapauth import *
import usermanager

__version__ = '0.0.1'

            
def prompt_user_info():
    name = raw_input('Input user name: ')
    while True:
        password = getpass.getpass('Input password: ')
        password_again = getpass.getpass('Input again:: ')
        if password == password_again: break
        else: print 'Password do not match!'
    dev = raw_input('Decice(eth0 by default): ')
    if not dev: dev = 'eth0'
    return name, password, dev


def main():
    # check for root privilege
    if not (os.getuid() == 0):
        print ('亲，要加sudo!')
        exit(-1)

    um = usermanager.UserManager()
    if (um.get_user_number() == 0):
        choice = raw_input('No user conf file found, creat a new one?\n<Y/N>: ')
        if choice == 'y' or choice == 'Y': 
            name, password, dev = prompt_user_info()
            um.create_user((name, password, dev))
            login_info['user'] = name
            login_info['password'] = password
            login_info['device'] = dev
        else: exit(-1)
    else: 
        users_info = um.get_users_info()

        print '0. add a new user'
        for i in range(len(users_info)):
            print i+1, users_info[i]

        while True:
            try:
                choice = int(raw_input('Your choice: '))
            except ValueError:
                print 'Please input a valid number!'
            else: break;
        if (choice == 0):
            try:
                name, password, dev = prompt_user_info()
                um.create_user((name, password, dev))
            except ConfigParser.DuplicateSectionError:
                print 'user already exist!'
        else: name, password, dev = um.get_user_info(choice-1)
        login_info['user'] = name
        login_info['password'] = password
        login_info['device'] = dev

    yah3c = EAPAuth()
    yah3c.serve_forever()


if __name__ == "__main__":
    main()
