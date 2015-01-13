/*
 * openssl_sha2.c
 *
 *  Created on: Oct 18, 2014
 *      Author: d
 */

#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>

int main()
{
    unsigned char ibuf[] = "This is a hashed message";
    unsigned char obuf[20];

    SHA2(ibuf, strlen(ibuf), obuf);

    int i;
    for (i = 0; i < 20; i++) {
        printf("%02x ", obuf[i]);
    }
    printf("\n");

    return 0;
}
