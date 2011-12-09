import ConfigParser
import os

class UserManager:
    def __init__(self):
        self.homedir = os.path.expanduser('~'+os.getenv('SUDO_USER'))
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.homedir + '/.yah3c/users.conf')
       
    def get_user_number(self):
        return len(self.cf.sections())

    def get_users_info(self):
        users_info = []
        for account in self.cf.sections():
            dev = self.cf.get(account, 'dev')
            users_info.append((account, dev))
        return users_info
    
    def create_user(self, user_info):
        self.cf.add_section(user_info[0])
        self.update_user_info(user_info)

    def update_user_info(self, user_info):
        self.cf.set(user_info[0], 'password', user_info[1])
        self.cf.set(user_info[0], 'dev', user_info[2])
        fp = open(self.homedir+'/.yah3c/users.conf', 'w')
        self.cf.write(fp)
        fp.close()

    def get_user_info(self, idx):
        account = self.cf.sections()[idx]
        password = self.cf.get(account, 'password')
        dev = self.cf.get(account, 'dev')
        return (account, password, dev)
         
