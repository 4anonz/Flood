#include "flood.h"

//Needed for checksum calculation
struct pseudo_header {
    u_int32_t source_address;
    u_int32_t destination_address;
    u_int8_t placeholder;
    u_int8_t protocol;
    u_int16_t tcp_length;
};
// For resolving hotnames to ip

//The function for performing checksum calculation
/**
 * Referene https://geeksforgeeks/ping-c
*/
unsigned short checksum(void *b, int len) {
    unsigned short *buf = b;
    unsigned int sum = 0;
    unsigned short result;

    for(sum = 0; len > 1; len -= 2)
        sum +=*buf++;
    if(len == 1)
        sum += *(unsigned char *)buf;
    sum = (sum >> 16) + (sum & 0xFFFF);
    sum += (sum >> 16);
    result = ~sum;
    return result;  

}

//Perform a DNS lookup to find host ip
char *dns_lookup(char *host, struct sockaddr_in *addr_conn) {
    struct hostent *host_e;
    char *ip = (char *) malloc(NI_MAXHOST*sizeof(char));

    host_e = gethostbyname(host);
    if(host_e == NULL)
        return NULL;
    strcpy(ip, inet_ntoa(*(struct in_addr*)host_e->h_addr));

    (*addr_conn).sin_family = host_e->h_addrtype;
    (*addr_conn).sin_port = htons(0);
    (*addr_conn).sin_addr.s_addr = *(long*)host_e->h_addr;
    return ip;
}

