#ifndef PACKT_H
#define PACKT_H

#include <string.h>
#include <stdlib.h>
#include <time.h>

#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <errno.h>
#include <netdb.h>
#include <netinet/ip.h>

const char *whi = "\033[1;37m",
//*grey = "\033[0;37m",
*pur = "\033[0;35m",
*red = "\033[1;31m",
*gre = "\033[1;32m",
*yel = "\033[1;33m",
*cyan = "\033[0;36m",
//*cafe = "\033[0;33m",
//*fiuscha = "\033[0;35m",
*blu = "\033[1;34m",
*res = "\e[0m";


/**
 * Function for returning a random number in range
*/
int random_range(int lower, int upper) {
    int rand_num;
    rand_num = (rand() % (upper - lower + 1)) + lower;
    return rand_num;
}

void print_status(char *);
unsigned short checksum(void *, int);

#endif /*PACKT_H*/