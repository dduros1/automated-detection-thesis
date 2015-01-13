/*
 * openssl_3des.c
 *
 *  Created on: Oct 18, 2014
 *      Author: d
 *
 *  All DES code created with the help of http://blog.fpmurphy.com/2010/04/openssl-des-api.html
 */

#include <unistd.h>
#include <openssl/des.h>

#define BUFSIZE 1024

int main(void)
{
    unsigned char in[BUFSIZE], encrypted[BUFSIZE], decrypted[BUFSIZE];
    unsigned char *e = encrypted;
    int len;

    DES_cblock key1, key2, key3;
    DES_cblock seed = {0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10};
    DES_key_schedule ks1, ks2, ks3;
    DES_cblock ivsetup = {0xE1, 0xE2, 0xE3, 0xD4, 0xD5, 0xC6, 0xC7, 0xA8};
    DES_cblock ivec;

    memset(in, 0, sizeof(in));
    memset(encrypted, 0, sizeof(encrypted));
    memset(decrypted, 0, sizeof(decrypted));

    RAND_seed(seed, sizeof(DES_cblock));

    DES_random_key(&key1);
    DES_random_key(&key2);
    DES_random_key(&key2);

    DES_set_key((DES_cblock *)key1, &ks1);
    DES_set_key((DES_cblock *)key2, &ks2);
    DES_set_key((DES_cblock *)key3, &ks3);

    /* plaintext */
    strcpy(in, "this is a string encrypted with triple des. it is 64 bytes long.");


    len = strlen(in);
    memcpy(ivec, ivsetup, sizeof(ivsetup));
    DES_ede3_cbc_encrypt(in, encrypted, len, &ks1, &ks2, &ks3, &ivec, DES_ENCRYPT);

    len = strlen(encrypted);
    memcpy(ivec, ivsetup, sizeof(ivsetup));
    DES_ede3_cbc_encrypt(encrypted, decrypted, len, &ks1, &ks2, &ks3, &ivec, DES_DECRYPT);

    printf("Decrypted Text: %s\n", decrypted);

    exit(0);


}




//int main() {
//	// set mode
//	/*
//	 * TODO make different code per option
//	 * int opt;
//	while ((opt = getopt(argc, argv, "cof")) != -1) {
//		switch (opt) {
//		case 'c':
//			mode = CBC_MODE;
//			break;
//		case 'o':
//			mode = OFB_MODE;
//			break;
//		case 'f':
//			mode = CFB_MODE;
//			break;
//		default:
//			mode = CBC_MODE;
//			break;
//		}
//	}*/
//
//	const unsigned char plaintext[] = "this is a string encrypted with 3des";
//	int bufsize = sizeof(plaintext);
//
//	//initialize
//	char iv;
//	des_cblock key1, key2, key3, seed = { 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54,
//			0x32, 0x10 };
//	DES_key_schedule * ks1, * ks2, * ks3;
//
//	des_random_seed(seed);
//	des_random_key(key1);
//	des_random_key(key2);
//	des_random_key(key3);
//
//	des_set_key((C_Block *)key1, ks1);
//	des_set_key((C_Block *)key2, ks2);
//	des_set_key((C_Block *)key3, ks3);
//
//	memset(iv, 0, bufsize);
//
////	//char key[] = "this is a bad password";
////
//	unsigned char * encrypted;
//	unsigned char * decrypted;
//
//	//compiler doesn't recognize these
////	DES_ed3_cbc_encrypt(plaintext, encrypted, bufsize, ks1, ks2, ks3, iv, 1);
////	DES_ed3_cbc_encrypt(encrypted, decrypted, bufsize, ks1, ks2, ks3, iv, 0);
//
//	DES_ede3_cbc_encrypt(plaintext,
//	        encrypted, (long) bufsize, ks1,
//	        ks2, ks3, iv,
//	        1);
////	DES_ede3_cbc_encrypt(encrypted,
////	        decrypted, (long) bufsize, ks1,
////	        ks2, ks3, iv,
////	        0);
//
//	printf("Decrypted: %s", decrypted);
//
////
////	encrypt(key, plaintext, *encrypted);
////
////	decrypt(key, encrypted, *decrypted);
//
//	return 0;
//}
