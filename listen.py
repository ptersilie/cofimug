from plug import decrypt
import socket

UDP_IP = ""
UDP_PORT = 8530

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "Received UDP message:"
    print "IP: %s" % (addr,)
    print "MAC: %s" % (":".join(["%02x" % ord(x) for x in data[2:8]]),)
    msg = decrypt(data[9:])
    print "Company code: %02x" % (ord(msg[3]),)
    print "Device type: %02x" % (ord(msg[4]),)
    print "Authcode: %02x%02x" % (ord(msg[5]), ord(msg[6]))
    switchmsg = [ord(x) for x in msg[7:]]
    switchmsg.append("ON" if ord(msg[10]) == 255 else "OFF")
    print "Message: %02x%02x%02x%02x%02x (%s)" % tuple(switchmsg)
    print ""
