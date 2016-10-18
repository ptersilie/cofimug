from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

def encrypt(msg):
    suite = AES.new("0123456789abcdef", AES.MODE_CBC, "0123456789abcdef")
    return suite.encrypt(pad(msg))

def decrypt(msg):
    suite = AES.new("0123456789abcdef", AES.MODE_CBC, "0123456789abcdef")
    s = suite.decrypt(msg)
    # remove padding
    s = s[0:-ord(s[-1])]
    return s

def switch_command(comp, dev, auth, mode):
    l = []
    l.append(0x00)
    l.append(0x00) # counter1
    l.append(0x00) # counter2
    l.append(int(comp, 16)) # company code
    l.append(int(dev, 16)) # device code
    l.append(int(auth[:2], 16)) # auth code1
    l.append(int(auth[2:], 16)) # auth code2
    l.append(0x01) # msg...
    l.append(0x00)
    l.append(0x00)
    if mode == "on":
        l.append(0xFF)
    else:
        l.append(0x00)
    l.append(0xFF)
    return "".join([chr(x) for x in l])

def mac_to_bytes(mac):
    l = []
    for x in mac.split(":"):
        l.append(int(x, 16))
    return "".join([chr(x) for x in l])

def create_header(mac):
    l = []
    l.append(chr(0x01))
    l.append(chr(0x40))
    l.append(mac_to_bytes(mac)) # MAC
    return "".join(l)

def switch(ip, mac, comp, dev, auth, mode):
    head = create_header(mac)
    msg = switch_command(comp, dev, auth, mode)
    enc_msg = encrypt(msg)
    sendudp("".join([head, chr(len(enc_msg)), enc_msg]), ip, 8530)

def sendudp(msg, ip, port):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg, (ip, port))

if __name__ == "__main__":
    import sys
    devicename = sys.argv[1]
    mode = sys.argv[2]

    from config import cfg
    device = cfg[devicename]
    msg = switch(device["ip"], device["mac"], device["companycode"], \
            device["devicecode"], device["authcode"], mode)
