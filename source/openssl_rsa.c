#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <openssl/evp.h>
#include <openssl/pem.h>

#define FAILURE -1
#define RSA_KEYLEN 2048


int rsa_init(EVP_CIPHER_CTX *encryptCtx, EVP_CIPHER_CTX * decryptCtx) {
    EVP_CIPHER_CTX_init(decryptCtx);
    EVP_CIPHER_CTX_init(encryptCtx);
}

int rsa_encrypt( EVP_CIPHER_CTX *encryptCtx, unsigned char remotePubKey, const unsigned char *msg, size_t msgLen, unsigned char **encMsg, unsigned char **ek, size_t *ekl, unsigned char **iv, size_t *ivl) {
    size_t encMsgLen = 0;
    size_t blockLen  = 0;

    *ek = (unsigned char*)malloc(EVP_PKEY_size(remotePubKey));
    *iv = (unsigned char*)malloc(EVP_MAX_IV_LENGTH);
    if(*ek == NULL || *iv == NULL) return FAILURE;
    *ivl = EVP_MAX_IV_LENGTH;

    *encMsg = (unsigned char*)malloc(msgLen + EVP_MAX_IV_LENGTH);
    if(encMsg == NULL) return FAILURE;

    if(!EVP_SealInit(encryptCtx, EVP_aes_256_cbc(), ek, (int*)ekl, *iv, &remotePubKey, 1)) {
        return FAILURE;
    }

    if(!EVP_SealUpdate(encryptCtx, *encMsg + encMsgLen, (int*)&blockLen, (const unsigned char*)msg, (int)msgLen)) {
        return FAILURE;
    }
    encMsgLen += blockLen;

    if(!EVP_SealFinal(encryptCtx, *encMsg + encMsgLen, (int*)&blockLen)) {
        return FAILURE;
    }
    encMsgLen += blockLen;

    EVP_CIPHER_CTX_cleanup(encryptCtx);

    return (int)encMsgLen;
}

int rsa_decrypt(EVP_CIPHER_CTX * decryptCtx, unsigned char localKeypair, unsigned char *encMsg, size_t encMsgLen, unsigned char *ek, size_t ekl, unsigned char *iv, size_t ivl, unsigned char **decMsg) {
    size_t decLen   = 0;
    size_t blockLen = 0;
    EVP_PKEY *key;

    *decMsg = (unsigned char*)malloc(encMsgLen + ivl);
    if(decMsg == NULL) return FAILURE;


    key = localKeypair;

    if(!EVP_OpenInit(decryptCtx, EVP_aes_256_cbc(), ek, ekl, iv, key)) {
        return FAILURE;
    }

    if(!EVP_OpenUpdate(decryptCtx, (unsigned char*)*decMsg + decLen, (int*)&blockLen, encMsg, (int)encMsgLen)) {
        return FAILURE;
    }
    decLen += blockLen;

    if(!EVP_OpenFinal(decryptCtx, (unsigned char*)*decMsg + decLen, (int*)&blockLen)) {
        return FAILURE;
    }
    decLen += blockLen;

    EVP_CIPHER_CTX_cleanup(decryptCtx);

    return (int)decLen;
}

/*
 * The RSA keys are just set to NULL because their values will be initialized later when the RSA/AES functions
 */
int main() {
	EVP_CIPHER_CTX * encryptCtx = (EVP_CIPHER_CTX*) malloc(
			sizeof(EVP_CIPHER_CTX));
	EVP_CIPHER_CTX * decryptCtx = (EVP_CIPHER_CTX*) malloc(
			sizeof(EVP_CIPHER_CTX));

	if (encryptCtx == NULL || decryptCtx == NULL) {
		return FAILURE;
	}

    unsigned char localKeypair  = NULL;
    unsigned char remotePubKey  = NULL;

    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_id(EVP_PKEY_RSA, NULL);

    if(EVP_PKEY_keygen_init(ctx) <= 0) {
        return FAILURE;
    }

    if(EVP_PKEY_CTX_set_rsa_keygen_bits(ctx, RSA_KEYLEN) <= 0) {
        return FAILURE;
    }

    if(EVP_PKEY_keygen(ctx, &localKeypair) <= 0) {
        return FAILURE;
    }

    EVP_PKEY_CTX_free(ctx);


    size_t remotePubKeyLen;
    setRemotePubKey(remotePubKey, remotePubKeyLen);


    //free everything
    EVP_PKEY_free(remotePubKey);

    EVP_CIPHER_CTX_cleanup(encryptCtx);
    EVP_CIPHER_CTX_cleanup(decryptCtx);

    free(encryptCtx);
    free(decryptCtx);

}
