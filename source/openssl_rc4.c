/*
 * openssl_rc4.c
 *
 *  Created on: Jan 13, 2015
 *      Author: d
 *
 *  http://webdev.sis.pitt.edu/st/crypto_libs/crypto2.htm
 */

#include <stdlib.h>
#include <openssl/rc4.h>

int main(void) {

	char plaintext[64] = "this is a string encrypted with openssl rc4. it is 64 bytes long.";
	char ciphertext[64];
	char mykey[16] = "this is a bad password";
	RC4_KEY rc4_key;

	RC4_set_key(&rc4_key, 16, mykey); /* the key is 128 bits or 16 bytes long */
	RC4(&rc4_key, 12, plaintext, ciphertext); /* plaintext is 12 bytes long */

//	printf("%s\n", plaintext);
//	printf("Encrypted: %s\n", ciphertext);

	RC4_set_key(&rc4_key, 16, mykey); /* reset the key stream */
	RC4(&rc4_key, 12, ciphertext, plaintext); /* start decryption */

	printf("Decrypted: %s\n", plaintext);

	exit(1);
}
