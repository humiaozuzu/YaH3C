from socket import *
from colorama import Fore, Style, init
# init() # required in Windows
from h3cPacket import *
import plugins

login_info = {
        "user": "your id",
        "password": "your password",
        "device": "eth0"
        }

def display_prompt(color, string):
    prompt = color + Style.BRIGHT + '==> ' + Style.RESET_ALL
    prompt += Style.BRIGHT + string + Style.RESET_ALL
    print prompt

def display_packet(packet):
    # print ethernet_header infomation
    print 'Ethernet Header Info: '
    print '\tFrom: ' + repr(packet[0:6])
    print '\tTo: ' + repr(packet[6:12])
    print '\tType: ' + repr(packet[12:14])

class YaH3C:
    def __init__(self):
        # bind the h3c client to the EAP protocal 
        self.client = socket(AF_PACKET, SOCK_RAW, htons(ETHERTYPE_PAE))
        self.client.bind((login_info["device"], ETHERTYPE_PAE))
        self.mac_addr = self.client.getsockname()[4]
        self.ethernet_header = get_ethernet_header(self.mac_addr, PAE_GROUP_ADDR, ETHERTYPE_PAE)
        self.loaded_plugins = []
        self.loading_plugins = ['test']

    def load_plugins(self):
        imported_plugins = __import__('plugins', globals(), locals(), self.loading_plugins)
        for plugin in self.loading_plugins:
            self.loaded_plugins.append(getattr(imported_plugins, plugin))


    def send_start(self):
        for plugin in self.loaded_plugins:
            getattr(plugin, 'before_auth')(self)
        eap_start_packet = self.ethernet_header + get_EAPOL(EAPOL_START)
        self.client.send(eap_start_packet)

        display_prompt(Fore.GREEN, 'Sending EOPAL start')

    def send_logoff(self):
        for plugin in self.loaded_plugins:
            getattr(plugin, 'before_auth')(self)
        eap_logoff_packet = self.ethernet_header + get_EAPOL(EAPOL_LOGOFF)
        self.client.send(eap_logoff_packet)

        display_prompt(Fore.GREEN, 'Sending EOPAL logoff')

    def EAP_handler(self, eap_packet):
        vers, type, eapol_len  = unpack("!BBH",eap_packet[:4])
        if type == EAPOL_EAPPACKET:
            code, id, eap_len = unpack("!BBH", eap_packet[4:8])
            if code == EAP_SUCCESS:
                display_prompt(Fore.YELLOW, 'Got EAP Success')
            elif code == EAP_FAILURE:
                display_prompt(Fore.YELLOW, 'Got EAP Failure')
                print eap_packet[10:].decode('gbk')
            elif code == EAP_RESPONSE:
                display_prompt(Fore.YELLOW, 'Got Unknown EAP Response')
            elif code == EAP_REQUEST:
                reqtype = unpack("!B", eap_packet[8:9])[0]
                reqdata = eap_packet[9:4 + eap_len]
                if reqtype == EAP_TYPE_ID:
                    display_prompt(Fore.YELLOW, 'Got EAP Request for identity')
                    self.client.send(self.ethernet_header + 
                            get_EAPOL(EAPOL_EAPPACKET,
                                get_EAP(EAP_RESPONSE,
                                    id,
                                    reqtype,
                                    '\x15\x04\x00\x00\x00\x00' + login_info['user'])))
                    display_prompt(Fore.GREEN, 'Sending EAP response with identity = [%s]' % login_info['user'])
                elif reqtype == EAP_TYPE_ALLOCATED:
                    display_prompt(Fore.YELLOW, 'Got EAP Request for Allocation')
                    resp=chr(len(login_info['password']))+login_info['password']+login_info['user']
                    eap_packet = self.ethernet_header + get_EAPOL(EAPOL_EAPPACKET, get_EAP(EAP_RESPONSE, id, reqtype, resp))
                    # print repr(eap_packet)
                    self.client.send(eap_packet)
                    display_prompt(Fore.GREEN, 'Sending EAP response with password')
                else:
                    display_prompt(Fore.YELLOW, 'Got unknown Request type (%i)' % reqtype)
            elif code==10 and id==5:
                print eap_packet[12:].decode('gbk')
            else:
                display_prompt(Fore.YELLOW, 'Got unknown EAP code (%i)' % code)
        else:
            display_prompt(Fore.YELLOW, 'Got unknown EAPOL type %i' % type)

    def serve_forever(self):
        try:
            self.load_plugins()
            self.send_start()
            while 1:
                eap_packet = self.client.recv(1600)
                display_packet(eap_packet)
                # strip the ethernet_header and handle
                self.EAP_handler(eap_packet[14:])
        except KeyboardInterrupt:
            print Fore.RED + Style.BRIGHT + 'Interrupted by user' + Style.RESET_ALL
            self.send_logoff()



if __name__ == "__main__":
    yah3c = YaH3C()
    yah3c.serve_forever()
