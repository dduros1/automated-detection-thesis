/*
 * openssl_sha1.c
 *
 *  Created on: Oct 16, 2014
 *      Author: d
 */

#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>

/**
 * Consider changing to use CTX objects
 */
int main()
{
    unsigned char ibuf[] = "This is a hashed message";
    unsigned char obuf[20];

    SHA1(ibuf, strlen(ibuf), obuf);

    int i;
    for (i = 0; i < 20; i++) {
        printf("%02x ", obuf[i]);
    }
    printf("\n");

    return 0;
}
