#!/usr/bin/python3

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
        print(f"{whi}Usage:{res} {sys.argv[0]} <IP(s)> <Output File>\n")
        sys.exit(1)
    net = str(sys.argv[1])
    output_file = str(sys.argv[2])


def form_bots():
    global net, ip_list
    try:
        # If many ip addresses is available
        if ',' in net:
            ip_addresses = net.split(',')
            for each_ip in ip_addresses:
                ip_split = each_ip.split('.')
                ip_split[3] = '0'
                for i in range(1, 256):
                    ip_split[3] = f'{i}'
                    ip_addr = ip_split[0]+'.'+ip_split[1]+'.'+ip_split[2]+'.'+ip_split[3]
                    ip_list.append(ip_addr)
        # Else if only one ip address is supplied
        else:
            ip_split = net.split('.')
            ip_split[3] = '0'
            for i in range(1, 256):
                ip_split[3] = f'{i}'
                ip_addr = ip_split[0]+'.'+ip_split[1]+'.'+ip_split[2]+'.'+ip_split[3]
                ip_list.append(ip_addr)

    except IndexError:
        print(f"{whi}[{red}ERROR{whi}]:{res} Invalid ip address(es) '{net}'")
        sys.exit(1)


if __name__ == '__main__':
    try:
        check_args()
        form_bots()
        
        file = open(output_file, "w")
        for ip in ip_list:
            file.write(ip)
            print(ip)
            file.write('\n')
        file.close()
    except KeyboardInterrupt:
        print(f"\n{whi}[{yel}CRITICAL{whi}]:{res} User aborted(Ctl+C)")
        sys.exit(1)