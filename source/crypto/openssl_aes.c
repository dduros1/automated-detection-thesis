/**
*
* code modified from http://pastebin.com/MA66Me5G and https://shanetully.com/2012/06/openssl-rsa-aes-and-c/
*
*
*/

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <openssl/aes.h>
#include <openssl/rand.h>
#include <openssl/evp.h>
#include <openssl/bio.h>

 
 
#define AES_BLOCK_SIZE 256
#define AES_ROUNDS 6
#define FAILURE -1

int aes_init(unsigned char *key, unsigned char *iv, EVP_CIPHER_CTX *encryptCtx, EVP_CIPHER_CTX * decryptCtx){


    EVP_CIPHER_CTX_init(encryptCtx);
    EVP_CIPHER_CTX_init(decryptCtx);

    if (RAND_bytes(key, AES_BLOCK_SIZE/8) == 0 || RAND_bytes(iv, AES_BLOCK_SIZE/8)== 0) {
        return FAILURE;
    }

    return 0;
}

int aes_encrypt(const unsigned char * message, size_t message_len, unsigned char ** cipher, EVP_CIPHER_CTX* encryptCtx, unsigned char * key, unsigned char * iv){
    size_t blockLen = 0;
    size_t c_len = 0;

    *cipher = (unsigned char *) malloc(message_len + AES_BLOCK_SIZE);
    if (cipher == NULL) return FAILURE;

    if(!EVP_EncryptInit_ex(encryptCtx, EVP_aes_256_cbc(), NULL, key, iv)) {
        return FAILURE;
    }
 
    if(!EVP_EncryptUpdate(encryptCtx, *cipher, (int*)&blockLen, (unsigned char*)message, message_len)) {
        return FAILURE;
    }
    c_len += blockLen;
 
    if(!EVP_EncryptFinal_ex(encryptCtx, *cipher + c_len, (int*)&blockLen)) {
        return FAILURE;
    }
 
    EVP_CIPHER_CTX_cleanup(encryptCtx);
 
    return c_len + blockLen;
    

}

int aes_decrypt(unsigned char * cipher, size_t c_len, unsigned char ** message, EVP_CIPHER_CTX* decryptCtx, unsigned char * aesKey, unsigned char * aesIV){

    size_t messageLen, blockLen = 0;

    *message = (unsigned char*) malloc(c_len);
    if (*message == NULL) return FAILURE;

    if(!EVP_DecryptInit_ex(decryptCtx, EVP_aes_256_cbc(), NULL, aesKey, aesIV)) {
        return FAILURE;
    }
 
    if(!EVP_DecryptUpdate(decryptCtx, (unsigned char*)*message, (int*)&blockLen, cipher, (int)c_len)) {
        return FAILURE;
    }
    messageLen += blockLen;
 
    if(!EVP_DecryptFinal_ex(decryptCtx, (unsigned char*)*message + messageLen, (int*)&blockLen)) {
        return FAILURE;
    }
    messageLen += blockLen;
    EVP_CIPHER_CTX_cleanup(decryptCtx);

    return (int) messageLen;

}

/*
 * TODO there's a bug in the decrypt (probably a length thing)
 *      also try to get base64 encoding working
 *
 */
int main(){

    /* Create context objects */
    EVP_CIPHER_CTX * encryptCtx = (EVP_CIPHER_CTX*)malloc(sizeof(EVP_CIPHER_CTX));
    EVP_CIPHER_CTX * decryptCtx = (EVP_CIPHER_CTX*)malloc(sizeof(EVP_CIPHER_CTX));
    
    if (encryptCtx == NULL || decryptCtx ==NULL){
        return FAILURE;
    }

    unsigned char * key = (unsigned char *) malloc(AES_BLOCK_SIZE/8);
    unsigned char * iv = (unsigned char *) malloc(AES_BLOCK_SIZE/8);

    if (key == NULL || iv == NULL){
        return FAILURE;
    }


    aes_init(key, iv, encryptCtx, decryptCtx);

    char message[] = "This is an encrypted test string";
    unsigned char * encryptMessage = NULL;
    char * decryptMessage = NULL;


    aes_encrypt((const unsigned char*) message, strlen(message)+1, &encryptMessage, encryptCtx, key, iv);
    
    aes_decrypt(encryptMessage, strlen(encryptMessage), (unsigned char **) &decryptMessage, decryptCtx, key, iv);
    printf("Decrypted message: %s\n", decryptMessage);


    free(key);
    free(iv); 
    free(encryptCtx);
    free(decryptCtx);   
    free(encryptMessage);
    free(decryptMessage);
    //free(b64str);
    encryptMessage = NULL;
    decryptMessage = NULL;
    //b64str = NULL;

    return 0;

}


