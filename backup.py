# TODO: save current configs from LAB devices
import telnetlib
import re


ipfile = open('ipaddr.txt', 'r')
ipfile_lines = ipfile.readlines()


def telnet_connection(addr, port):
    tn = telnetlib.Telnet(addr, port, timeout=3)
    tn.debuglevel(100)


for line in ipfile_lines:
    line = line.rstrip()
    host_port = re.sub(r'[=,:,\s]', ' ', line)
    host = host_port.split(" ")[0]
    addr = host_port.split(" ")[1]
    port = host_port.split(" ")[2]
