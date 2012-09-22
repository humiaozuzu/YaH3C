""" User Management Module

This module reads the 'users.conf' file and gets all users's info.
"""

__all__ = ["UserMgr"]

import ConfigParser

class UserMgr:
    """User Manager
    The format of the user_info is:
    user_info = {
        "username": "maple",
        "password": "valley",
        "ethernet_interface": "eth0",
        "carry_version_info": true,
        "broadcast_logoff": false
        "packet_type": "unicast"
    }
    """
    def __init__(self, path=None):
        if path is None:
            self.users_cfg_path = '/etc/yah3c.conf'
        else:
            self.users_cfg_path = path
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.users_cfg_path)
       
    def get_user_number(self):
        return len(self.config.sections())

    def get_all_users_info(self):
        users_info = []
        for username in self.config.sections():
            user_info = dict(self.config.items(username))
            user_info['username'] = username
            users_info.append(user_info)

        return users_info

    def get_user_info(self, username):
        return dict(self.config.items(username))
    
    def add_user(self, user_info):
        self.config.add_section(user_info['username'])
        self.update_user_info(user_info)

    def remove_user(self, username):
        self.config.remove_section(username)
        fp = open(self.users_cfg_path, 'w')
        self.config.write(fp)
        fp.close()

    def update_user_info(self, user_info):
        self.config.set(user_info['username'], 'password',
                        user_info['password'])
        self.config.set(user_info['username'], 'ethernet_interface',
                        user_info['ethernet_interface'])
        fp = open(self.users_cfg_path, 'w')
        self.config.write(fp)
        fp.close()
