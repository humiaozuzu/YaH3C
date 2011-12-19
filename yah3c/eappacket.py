from struct import *

## Constants
# Reference: http://tools.ietf.org/html/rfc3748
ETHERTYPE_PAE = 0x888e
PAE_GROUP_ADDR = "\x01\x80\xc2\x00\x00\x03"
BROADCAST_ADDR = "\xff\xff\xff\xff\xff\xff"

EAPOL_VERSION = 1
EAPOL_EAPPACKET = 0

# packet info for EAPOL_EAPPACKET
EAPOL_START = 1
EAPOL_LOGOFF = 2
EAPOL_KEY = 3
EAPOL_ASF = 4

EAP_REQUEST = 1
EAP_RESPONSE = 2
EAP_SUCCESS = 3
EAP_FAILURE = 4

# packet info followed by EAP_RESPONSE
# 1       Identity
# 2       Notification
# 3       Nak (Response only)
# 4       MD5-Challenge
# 5       One Time Password (OTP)
# 6       Generic Token Card (GTC)
# 254     Expanded Types
# 255     Experimental use
EAP_TYPE_ID = 1                # identity
EAP_TYPE_MD5 = 4               # md5 Challenge
EAP_TYPE_H3C = 7               # H3C eap packet(used for SYSU east campus)

### Packet builders
def get_EAPOL(type, payload=""):
    return pack("!BBH", EAPOL_VERSION, type, len(payload))+payload

def get_EAP(code, id, type=0, data=""):
    if code in [EAP_SUCCESS, EAP_FAILURE]:
        return pack("!BBH", code, id, 4)
    else:
        return pack("!BBHB", code, id, 5+len(data), type)+data

def get_ethernet_header(src, dst, type):
    return dst+src+pack("!H",type)
