/*
 * openssl_3des_cfb.c
 *
 *  Created on: Jan 13, 2015
 *      Author: d
 *  All DES code created with the help of http://blog.fpmurphy.com/2010/04/openssl-des-api.html
 *
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <openssl/des.h>
#include <openssl/rand.h>

#define BUFSIZE 256
#define CFBMODE 1

int main(void)
{
    unsigned char in[BUFSIZE], encrypted[BUFSIZE], decrypted[BUFSIZE];
    unsigned char *e = encrypted;
    int len;

    DES_cblock key;
    DES_cblock seed = {0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10};
    DES_cblock ivecstr = {0xE1, 0xE2, 0xE3, 0xD4, 0xD5, 0xC6, 0xC7, 0xA8};
    DES_cblock ivec;
    DES_key_schedule ks;

    memset(in, 0, sizeof(in));
    memset(encrypted, 0, sizeof(encrypted));
    memset(decrypted, 0, sizeof(decrypted));

    RAND_seed(seed, sizeof(DES_cblock));

    DES_random_key(&key);
    DES_set_key((C_Block *)key, &ks);

    strcpy(in, "this is a string encrypted with triple des. it is 64 bytes long.");

    memcpy(ivec, ivecstr, sizeof(ivecstr));
    len = strlen(in);

    DES_cfb_encrypt(in, encrypted, CFBMODE, len, &ks, &ivec, DES_ENCRYPT);

    len = strlen(encrypted);
    memcpy(ivec, ivecstr, sizeof(ivecstr));

    DES_cfb_encrypt(encrypted, decrypted, CFBMODE, len, &ks, &ivec, DES_DECRYPT);

    printf("Decrypted Text: %s\n", decrypted);

    exit(0);
}



