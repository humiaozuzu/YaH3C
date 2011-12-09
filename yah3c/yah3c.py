#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" Main program for YaH3C.

"""

__version__ = '0.1'

import os, sys
import ConfigParser
import getpass
from socket import *

import eapauth
import usermanager
            
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
    login_info = []
    if (um.get_user_number() == 0):
        choice = raw_input('No user conf file found, creat a new one?\n<Y/N>: ')
        if choice == 'y' or choice == 'Y': 
            login_info = prompt_user_info()
            um.create_user(login_info)
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
                login_info = prompt_user_info()
                um.create_user(login_info)
            except ConfigParser.DuplicateSectionError:
                print 'user already exist!'
        else: login_info =  um.get_user_info(choice-1)

    yah3c = eapauth.EAPAuth(login_info)
    yah3c.serve_forever()


if __name__ == "__main__":
    main()
