#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" Main program for YaH3C.

"""

__version__ = '0.5'

import os, sys
import configparser
import getpass
import argparse
import logging

from . import eapauth
from . import usermgr


def parse_arguments():
    parser = argparse.ArgumentParser(description='Yet Another H3C Authentication Client', prog='yah3c')
    parser.add_argument('-u', '--username',
            help='Login in with this username')
    # parser.add_argument('-p', '--password',
    #         help='Password')
    # parser.add_argument('-i', '--interface', default='eth0',
    #         help='Etherent interface used. Set as eth0 by default.')
    # parser.add_argument('-d', '--daemon', action='store_true',
    #         help='Fork to background after authentication.')
    # parser.add_argument('-D', '--dhcp',
    #         help='DHCP cmd used to obtain ip after authentication.')
    parser.add_argument('-debug', action='store_true',
            help='Enable debugging mode')
    args = parser.parse_args()
    return args

def prompt_user_info():
    username = input('Input username: ')
    while True:
        password = getpass.getpass('Input password: ')
        password_again = getpass.getpass('Input again: ')
        if password == password_again:
            break
        else:
            print('Password do not match!')

    dev = input('Decice(eth0 by default): ')
    if not dev:
        dev = 'eth0'

    choice = input('Forked to background after authentication(Yes by default)\n<Y/N>: ')
    if choice == 'n' or choice == 'N':
        daemon = "False"
    else:
        daemon = "True"

    dhcp_cmd = input('Dhcp command(Press Enter to pass): ')
    if not dhcp_cmd:
        dhcp_cmd = ''
    return {
        'username': username,
        'password': password,
        'ethernet_interface': dev,
        'daemon': daemon,
        'dhcp_command': dhcp_cmd
    }

def enter_interactive_usermanager():
    um = usermgr.UserMgr()

    if um.get_user_number() == 0:
        choice = input('No user conf file found, creat a new one?\n<Y/N>: ')
        if choice == 'y' or choice == 'Y':
            login_info = prompt_user_info()
            um.add_user(login_info)
        else:
            exit(-1)

    # user has been created or already have users
    while True:
        users_info = um.get_all_users_info()

        print('0 - add a new user')
        for i, user_info in enumerate(users_info):
            print('%d - %s(%s)' %(i + 1, user_info['username'], user_info['ethernet_interface']))

        try:
            choice = int(input('Your choice: '))
        except ValueError:
            print('Please input a valid number!')
            continue

        if choice == 0:
            try:
                user_info = prompt_user_info()
                um.add_user(user_info)
            except configparser.DuplicateSectionError:
                print('User already exist!')
                exit(-1)
        else:
            return users_info[choice - 1]

def start_yah3c(login_info):
    yah3c = eapauth.EAPAuth(login_info)
    yah3c.serve_forever()

def main():
    args = parse_arguments()
    args = vars(args)

    # check for root privilege
    if not (os.getuid() == 0):
        print ('亲，要加sudo!')
        exit(-1)

    # check if debugging mode enabled
    if args['debug'] is True:
        logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')
        logging.debug('Debugging mode enabled.')
        logging.debug(args)

    # if no username specified then enter interactive mode
    if args['username'] is None:
        login_info = enter_interactive_usermanager()
        logging.debug(login_info)
        start_yah3c(login_info)

    # if there is username, then get it's info
    um = usermgr.UserMgr()
    login_info = um.get_user_info(args['username'])
    logging.debug(login_info)
    start_yah3c(login_info)

if __name__ == "__main__":
    main()
