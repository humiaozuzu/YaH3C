#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" Main program for YaH3C.

"""

__version__ = '0.4'

import os, sys
import ConfigParser
import getpass
from socket import socket

import eapauth
import usermgr
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Yet Another H3C.', prog='yah3c')
    parser.add_argument('-u', '--username',
            help='auth username')
    parser.add_argument('-p', '--password',
            help='auth password')
    parser.add_argument('-i', '--interface', default='eth0',
            help='Etherent interface used to send packet.eth0 by default.')
    parser.add_argument('-d', '--daemon', action='store_true',
            help='Go to background after authentication.')
    args = parser.parse_args()
    print args

def prompt_user_info():
    username = raw_input('Input username: ')
    while True:
        password = getpass.getpass('Input password: ')
        password_again = getpass.getpass('Input again: ')
        if password == password_again:
            break
        else:
            print 'Password do not match!'
    dev = raw_input('Decice(eth0 by default): ')
    if not dev:
        dev = 'eth0'
    return {
        'username': username,
        'password': password,
        'ethernet_interface': dev
    }

def enter_interactive_usermanager():
    um = usermgr.UserMgr()

    if um.get_user_number() == 0:
        choice = raw_input('No user conf file found, creat a new one?\n<Y/N>: ')
        if choice == 'y' or choice == 'Y': 
            login_info = prompt_user_info()
            um.add_user(login_info)
        else: 
            exit(-1)
    
    # user has been created or already have users
    users_info = um.get_all_users_info()

    print '0 - add a new user'
    for i, user_info in enumerate(users_info):
        print '%d - %s(%s)' %(i + 1, user_info['username'], user_info['ethernet_interface'])

    while True:
        try:
            choice = int(raw_input('Your choice: '))
        except ValueError:
            print 'Please input a valid number!'
        else: break;
    if choice == 0:
        try:
            user_info = prompt_user_info()
            um.add_user(user_info)
        except ConfigParser.DuplicateSectionError:
            print 'User already exist!'
            exit(-1)
    else: 
        return users_info[choice - 1]

def main():
    # TODO: combine cli args with config
    args = parse_arguments()

    # check for root privilege
    if not (os.getuid() == 0):
        print (u'亲，要加sudo!')
        exit(-1)

    if len(sys.argv) == 1:
        # enter interactive mode
        login_info = enter_interactive_usermanager()

    yah3c = eapauth.EAPAuth(login_info)
    yah3c.serve_forever()


if __name__ == "__main__":
    main()
