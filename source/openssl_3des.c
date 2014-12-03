/*
 * openssl_3des.c
 *
 *  Created on: Oct 18, 2014
 *      Author: d
 */

#include <unistd.h>


/**
 * Use a #define to select cbc, ofb, cfb
 * argument parsing to select via command line
 */
#define CBC

enum { CBC_MODE, OFB_MODE, CFB_MODE } mode = CBC_MODE;


int encrypt(char * key, char * message, char ** encMsg){

	switch(mode){
	case CBC_MODE: break;
	case OFB_MODE: break;
	case CFB_MODE: break;
	}

	return strlen(*encMsg);
}


int decrypt(char * key, char * message, char ** decMsg){

	switch(mode){
	case CBC_MODE: break;
	case OFB_MODE: break;
	case CFB_MODE: break;
	}

	return strlen(*decMsg);
}


int main(int argc, char *argv[]){
	// set mode
    int opt;
    while ((opt = getopt(argc, argv, "cof")) != -1) {
        switch (opt) {
        case 'c': mode = CBC_MODE; break;
        case 'o': mode = OFB_MODE; break;
        case 'f': mode = CFB_MODE; break;
        default:
            mode=CBC_MODE; break;
        }


	char key[] = "this is a bad password";
	char plaintext[] = "this is a string encrypted with 3des";

	char * encrypted;
	char * decrypted;

	encrypt(key, plaintext, *encrypted);

	decrypt(key, encrypted, *decrypted);

}
