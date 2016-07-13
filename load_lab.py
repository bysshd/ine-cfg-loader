from os import listdir
from os import getenv
from os import remove
from ciscoconfparse import CiscoConfParse
import re
import telnetlib
import time

# folder with INE configs

path = getenv("HOME") + '/configs/'

ipfile = open('ipaddr.txt', 'r')
ipfile_lines = ipfile.readlines()


# convert list path to dict

def path_to_dict(path_list):
    key = 1
    path_dict = {}
    for i in path_list:
        path_dict[key] = i
        key += 1
    return path_dict


# print path dict

def print_path_to_dict(path_dict):
    for num in path_dict:
        print("%s : %s" % (num, path_dict[num]))


list_path = listdir(path)
list_path.sort()
path_dict = path_to_dict(list_path)
print_path_to_dict(path_dict)

select = input("Enter Lab: ")
# selected directory

selected_directory = path_dict[int(select)]
main_folder = selected_directory
print("=====" + selected_directory.upper() + "=====")
selected_directory = path + selected_directory + "/"
print(selected_directory)

# working with subfolder

selected_lab = listdir(selected_directory)
selected_lab.sort()
path_dict = path_to_dict(selected_lab)
print_path_to_dict(path_dict)

# select lab

select = input("Enter Lab Number: ")
selected_lab = path_dict[int(select)]
lab_folder = selected_directory + selected_lab + "/"
print("=====" + selected_lab.upper() + "=====")
print(lab_folder)


def parse_config(host, addr):
    # search mngmt interface in .txt files
    # interface GigabitEthernet3 is MNGMNT interface
    txt_cfg = lab_folder + host + ".txt"
    mngmnt_interface = "GigabitEthernet3"
    ip_param = "ip address " + addr + " 255.255.255.0"

    parse = CiscoConfParse(txt_cfg, factory=True)
    interface = parse.find_interface_objects(mngmnt_interface)
    # add interface gig3

    if interface == []:
        print("creating mngmnt interface")
        parse.insert_before('line con 0', 'interface GigabitEthernet3')
        parse.commit()

        for obj in parse.find_interface_objects(mngmnt_interface):
            obj.append_to_family('!')
            obj.append_to_family(' no shutdown')
            obj.append_to_family(' ' + ip_param)
            obj.append_to_family(' description MNGMNT')

        parse.commit()
        parse.save_as(txt_cfg)
    else:
        print("Interface already configured")
        pass

def telnet_connection(host, addr, port):
    conf_replace = "configure replace http://192.168.182.42/configs/"
    http = conf_replace + main_folder + "/" + selected_lab + "/" + host + ".txt" + " " + "force"
    cmd_file = open(host + '_cmd.txt', 'a+')
    cmd_file.write(http)
    cmd_file.seek(0)

    tn = telnetlib.Telnet(addr, port, timeout=5)
    tn.set_debuglevel(100)

    for each_line in cmd_file.readlines():
        tn.write(each_line.encode('ascii') + b"\n")
        time.sleep(2)
        tn.write(b"\n")
        time.sleep(1)
        tn.write(b"\n")
        time.sleep(1)
        tn.write(b"\n")
        time.sleep(1)
        tn.read_until(b"#")
        time.sleep(1)

    cmd_file.close()
    tn.close()


for line in ipfile_lines:
    line = line.rstrip()
    host_port = re.sub(r'[=,:,\s]', ' ', line)
    host = host_port.split(" ")[0]
    addr = host_port.split(" ")[1]
    port = host_port.split(" ")[2]

    parse_config(host, addr)
    telnet_connection(host, addr, port)

ipfile.close()