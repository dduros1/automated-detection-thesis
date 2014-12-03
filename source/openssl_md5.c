/*
 * openssl_md5.c
 *
 *  Created on: Oct 18, 2014
 *      Author: d
 */

#include <stdio.h>
#include <string.h>
#include <openssl/md5.h>

int main()
{
    unsigned char ibuf[] = "This is a hashed message";
    unsigned char obuf[20];

    MD5(ibuf, strlen(ibuf), obuf);

    int i;
    for (i = 0; i < 20; i++) {
        printf("%02x ", obuf[i]);
    }
    printf("\n");

    return 0;
}
