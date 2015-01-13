/*
 * openssl_3des.c
 *
 *  Created on: Oct 18, 2014
 *      Author: d
 *
 *  All DES code created with the help of http://blog.fpmurphy.com/2010/04/openssl-des-api.html
 */


#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <openssl/des.h>
#include <openssl/rand.h>

#define BUFSIZE 512

int main(void)
{
    unsigned char in[BUFSIZE], encrypted[BUFSIZE], decrypted[BUFSIZE];
    unsigned char *e = encrypted;
    int len;

    DES_cblock key1, key2, key3;
    DES_cblock seed = {0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10};
    DES_cblock ivecstr = {0xE1, 0xE2, 0xE3, 0xD4, 0xD5, 0xC6, 0xC7, 0xA8};
    DES_cblock ivec2, ivec1;
    DES_key_schedule ks1, ks2, ks3;

    memset(in, 0, sizeof(in));
    memset(encrypted, 0, sizeof(encrypted));
    memset(decrypted, 0, sizeof(decrypted));

    RAND_seed(seed, sizeof(DES_cblock));

    DES_random_key(&key1);
    DES_random_key(&key2);
    DES_random_key(&key3);

    DES_set_key((C_Block *)key1, &ks1);
    DES_set_key((C_Block *)key2, &ks2);
    DES_set_key((C_Block *)key3, &ks3);

    strcpy(in, "this is a string encrypted with triple des. it is 64 bytes long.");


    memcpy(ivec2, ivecstr, sizeof(ivecstr));
    memset(ivec1,'\0',sizeof(ivec2));
    len = strlen(in) + 1;

    DES_ede3_cbcm_encrypt(in, encrypted, len, &ks1, &ks2, &ks3, &ivec2, &ivec1, DES_ENCRYPT);

    len = strlen(encrypted) + 1;
    memcpy(ivec2, ivecstr, sizeof(ivecstr));
    memset(ivec1,'\0',sizeof(ivec2));

    DES_ede3_cbcm_encrypt(encrypted, decrypted, len, &ks1, &ks2, &ks3, &ivec2, &ivec1, DES_DECRYPT);

    printf("Decrypted Text: %s\n", decrypted);

    exit(0);

}
