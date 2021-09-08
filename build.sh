#!/bin/bash
echo "flood v0.0.1"
echo "Author: Anonymous Hacks(4anoz)"
echo "Github: https://github.com/4anonz"
echo "===> ABOUT <==="
echo "flood is a tool supporting some the most popular DDoS(Destributed denail of service)"
echo "flood supports The following DoS and DDoS attacks."
echo "HTTP GET request flood DoS attack"
echo "ICMP ping flood DDoS attack"
echo "TCP PSH+ACK flood DDoS attack"
echo "TCP SYN flood DDoS attack"
echo "UDP flood DoS attack"
echo "For more information and how to use this tool see https://github.com/4anonz/flood"
echo "===> DISCLAIMER <==="
echo "By proceeding you accept and agree that you're be helt accountable for any illegal usage."
echo "Use this tool for only pentesting and in ethical way!. Do not use it on any network you don't"
echo "have permission to."

read -p "Do you agree to use this tool in a legal way?(Y/n): " answer

if [[ "$answer" == "y" ]]||[[ "$answer" == "Y" ]]; then
	echo "Compiling...."
	mkdir bin
	echo "gcc src/icmp_flood.c -lpthread -o bin/icmp_flood"
	gcc src/icmp_flood.c -lpthread -o bin/icmp_flood
	echo "gcc src/tcp_ack_syn_flood.c -lpthread -o bin/tcp_psh_flood"
	gcc src/tcp_psh_ack_flood.c -lpthread -o bin/tcp_psh_flood
	echo "gcc src/tcp_syn_flood.c -lpthread -o bin/tcp_syn_flood"
	gcc src/tcp_syn_flood.c -lpthread -o bin/tcp_syn_flood
	echo "gcc src/udp_flood.c -lpthread -o bin/udp_flood"
	gcc src/udp_flood.c -lpthread -o bin/udp_flood
else
	exit 0
fi

echo "chmod +x flood.py" 
chmod +x flood.py
echo "Finished compiling[✔]"
exit 0
