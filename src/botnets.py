#!/usr/bin/python3
# This script is use for finding botnets to be use for the DDoS attack

from os import system
from xml.dom import minidom
import subprocess
import sys

net = ""
output_file = ""
ip_list = list()

whi = "\033[1;37m"
red = "\033[1;31m"
gre = "\033[0;32m"
yel = "\033[1;33m"
res = "\033[0;37;40m"

def check_args():
    global net, output_file, ip_list
    if len(sys.argv) != 3:
        print(f"{whi}[{yel}CRITICAL{whi}]:{res} Missing arguments..")
        print(f"{whi}Usage:{res} {sys.argv[0]} <IP> <Output File>\n")
        sys.exit(1)
    net = str(sys.argv[1])
    output_file = str(sys.argv[2])


def find_bots():
    global net
    dot = net.split('.')
    try:
        dot[3] = '0'
    except IndexError:
        print(f"{whi}[{red}ERROR{whi}]:{res} Invalid ip address '{net}'")
        sys.exit(1)
    ip = dot[0]+'.'+dot[1]+'.'+dot[2]+'.'+dot[3]+'/24'
    system(f'nmap -sA {ip} -oX nmapScan.xml')
    # output = subprocess.run(['nmap', '-sA', ip, '-oX', "nmapScan.xml"], capture_output=True)

    bots_list = minidom.parse('nmapScan.xml')
    bots = bots_list.getElementsByTagName('host')
    ip_addr = ""
    for node in bots:
        check = node.getElementsByTagName('extraports')
        for each in check:
            state = each.getAttribute('state')
            if state == 'unfiltered':
                address = node.getElementsByTagName('address')
                for ip in address:
                    ip_addr = str(ip.getAttribute('addr'))
                    ip_list.append(ip_addr)
                    print(ip_addr)


if __name__ == '__main__':
    try:
        check_args()
        find_bots()
        
        if not ip_list:
            print(f"{whi}[{yel}CRITICAL{whi}]:{res} No botnets found in this IP {gre}{net}{gre}")
            sys.exit(0)
        file = open(output_file, "w")
        for ip in ip_list:
            file.write(ip)
            file.write('\n')
        file.close()
    except KeyboardInterrupt:
        print(f"\n{whi}[{yel}CRITICAL{whi}]:{res} User aborted(Ctl+C)")
        sys.exit(1)
