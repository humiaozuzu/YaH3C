""" EAP authentication handler

This module sents EAPOL begin/logoff packet
and parses received EAP packet

"""

__all__ = ["EAPAuth"]

import socket
import os, sys, pwd
from subprocess import call

from .colorama import Fore, Style, init
# init() # required in Windows
from .eappacket import *

def display_prompt(color, string):
    prompt = color + Style.BRIGHT + '==> ' + Style.RESET_ALL
    prompt += Style.BRIGHT + string + Style.RESET_ALL
    print(prompt)

def display_packet(packet):
    # print ethernet_header infomation
    print('Ethernet Header Info: ')
    print('\tFrom: ' + repr(packet[0:6]))
    print('\tTo: ' + repr(packet[6:12]))
    print('\tType: ' + repr(packet[12:14]))

class EAPAuth:
    def __init__(self, login_info):
        # bind the h3c client to the EAP protocal
        self.client = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETHERTYPE_PAE))
        self.client.bind((login_info['ethernet_interface'], ETHERTYPE_PAE))
        # get local ethernet card address
        self.mac_addr = self.client.getsockname()[4]
        self.ethernet_header = get_ethernet_header(self.mac_addr, PAE_GROUP_ADDR, ETHERTYPE_PAE)
        self.has_sent_logoff = False
        self.login_info = login_info
        self.version_info = '\x06\x07bjQ7SE8BZ3MqHhs3clMregcDY3Y=\x20\x20'

    def send_start(self):
        # sent eapol start packet
        eap_start_packet = self.ethernet_header + get_EAPOL(EAPOL_START)
        self.client.send(eap_start_packet)

        display_prompt(Fore.GREEN, 'Sending EAPOL start')

    def send_logoff(self):
        # sent eapol logoff packet
        eap_logoff_packet = self.ethernet_header + get_EAPOL(EAPOL_LOGOFF)
        self.client.send(eap_logoff_packet)
        self.has_sent_logoff = True

        display_prompt(Fore.GREEN, 'Sending EAPOL logoff')

    def send_response_id(self, packet_id):
        self.client.send(self.ethernet_header +
                get_EAPOL(EAPOL_EAPPACKET,
                    get_EAP(EAP_RESPONSE,
                        packet_id,
                        EAP_TYPE_ID,
                        self.version_info + self.login_info['username'])))

    def send_response_md5(self, packet_id, md5data):
        md5 = self.login_info['password'][0:16]
        if len(md5) < 16:
            md5 = md5 + '\x00' * (16 - len (md5))
        chap = []
        for i in range(0, 16):
            chap.append(chr(ord(md5[i]) ^ md5data[i]))
        resp = chr(len(chap)) + ''.join(chap) + self.login_info['username']
        eap_packet = self.ethernet_header + get_EAPOL(EAPOL_EAPPACKET, get_EAP(EAP_RESPONSE, packet_id, EAP_TYPE_MD5, resp))
        try:
            self.client.send(eap_packet)
        except socket.error as msg:
            print("Connection error!")
            exit(-1)

    def send_response_h3c(self, packet_id):
        resp = chr(len(self.login_info['password'])) + self.login_info['password'] + self.login_info['username']
        eap_packet = self.ethernet_header + get_EAPOL(EAPOL_EAPPACKET, get_EAP(EAP_RESPONSE, packet_id, EAP_TYPE_H3C, resp))
        try:
            self.client.send(eap_packet)
        except socket.error as msg:
            print("Connection error!")
            exit(-1)

    def display_login_message(self, msg):
        """
            display the messages received form the radius server,
            including the error meaasge after logging failed or
            other meaasge from networking centre
        """
        try:
            print(msg.decode('gbk'))
        except UnicodeDecodeError:
            print(msg)

    def EAP_handler(self, eap_packet):
        vers, type, eapol_len  = unpack("!BBH",eap_packet[:4])
        if type != EAPOL_EAPPACKET:
            display_prompt(Fore.YELLOW, 'Got unknown EAPOL type %i' % type)

        # EAPOL_EAPPACKET type
        code, id, eap_len = unpack("!BBH", eap_packet[4:8])
        if code == EAP_SUCCESS:
            display_prompt(Fore.YELLOW, 'Got EAP Success')

            if self.login_info['dhcp_command']:
                display_prompt(Fore.YELLOW, 'Obtaining IP Address:')
                call([self.login_info['dhcp_command'], self.login_info['ethernet_interface']])

            if self.login_info['daemon'] == 'True':
                daemonize('/dev/null','/tmp/daemon.log','/tmp/daemon.log')

        elif code == EAP_FAILURE:
            if (self.has_sent_logoff):
                display_prompt(Fore.YELLOW, 'Logoff Successfully!')

                #self.display_login_message(eap_packet[10:])
            else:
                display_prompt(Fore.YELLOW, 'Got EAP Failure')

                #self.display_login_message(eap_packet[10:])
            exit(-1)
        elif code == EAP_RESPONSE:
            display_prompt(Fore.YELLOW, 'Got Unknown EAP Response')
        elif code == EAP_REQUEST:
            reqtype = unpack("!B", eap_packet[8:9])[0]
            reqdata = eap_packet[9:4 + eap_len]
            if reqtype == EAP_TYPE_ID:
                display_prompt(Fore.YELLOW, 'Got EAP Request for identity')
                self.send_response_id(id)
                display_prompt(Fore.GREEN, 'Sending EAP response with identity = [%s]' % self.login_info['username'])
            elif reqtype == EAP_TYPE_H3C:
                display_prompt(Fore.YELLOW, 'Got EAP Request for Allocation')
                self.send_response_h3c(id)
                display_prompt(Fore.GREEN, 'Sending EAP response with password')
            elif reqtype == EAP_TYPE_MD5:
                data_len = unpack("!B", reqdata[0:1])[0]
                md5data = reqdata[1:1 + data_len]
                display_prompt(Fore.YELLOW, 'Got EAP Request for MD5-Challenge')
                self.send_response_md5(id, md5data)
                display_prompt(Fore.GREEN, 'Sending EAP response with password')
            else:
                display_prompt(Fore.YELLOW, 'Got unknown Request type (%i)' % reqtype)
        elif code==10 and id==5:
            self.display_login_message(eap_packet[12:])
        else:
            display_prompt(Fore.YELLOW, 'Got unknown EAP code (%i)' % code)

    def serve_forever(self):
        try:
            self.send_start()
            while True:
                eap_packet = self.client.recv(1600)

                # strip the ethernet_header and handle
                self.EAP_handler(eap_packet[14:])
        except KeyboardInterrupt:
            print(Fore.RED + Style.BRIGHT + 'Interrupted by user' + Style.RESET_ALL)
            self.send_logoff()
        except socket.error as msg:
            print("Connection error: %s" %msg)
            exit(-1)

def daemonize (stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):

    '''This forks the current process into a daemon. The stdin, stdout, and
    stderr arguments are file names that will be opened and be used to replace
    the standard file descriptors in sys.stdin, sys.stdout, and sys.stderr.
    These arguments are optional and default to /dev/null. Note that stderr is
    opened unbuffered, so if it shares a file with stdout then interleaved
    output may not appear in the order that you expect. '''

    # Do first fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)   # Exit first parent.
    except OSError as e:
        sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror) )
        sys.exit(1)

    # Decouple from parent environment.
    os.chdir("/")
    os.umask(0)
    os.setsid()

    # Do second fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)   # Exit second parent.
    except OSError as e:
        sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror) )
        sys.exit(1)

    # Now I am a daemon!

    # Redirect standard file descriptors.
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'ab+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
