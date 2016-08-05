# TODO: save current configs from LAB devices
import time
import telnetlib
import re

ipfile = open('ipaddr.txt', 'r')
ipfile_lines = ipfile.readlines()

cmd = "copy running-config http://192.168.182.42/"


def telnet_connection(addr, port):
    tn = telnetlib.Telnet(addr, port, timeout=2)
    tn.debuglevel(100)
    time.sleep(1)
    tn.read_until(b"#")
    time.sleep(1)


for line in ipfile_lines:
    line = line.rstrip()
    host_port = re.sub(r'[=,:,\s]', ' ', line)
    host = host_port.split(" ")[0]
    addr = host_port.split(" ")[1]
    port = host_port.split(" ")[2]
