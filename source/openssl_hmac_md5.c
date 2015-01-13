/*
 * openssl_hmac_md5.c
 *
 *  Created on: Jan 13, 2015
 *      Author: d
 */


#include <stdio.h>
#include <string.h>
#include <openssl/hmac.h>

int main() {
    const char key[] = "this is a bad password";

    char plaintext[] = "this is a hashed string";

    unsigned char* result;
    unsigned int len = strlen(plaintext);

    result = (unsigned char*)malloc(sizeof(char) * len);

    HMAC_CTX ctx;
    HMAC_CTX_init(&ctx);

    HMAC_Init_ex(&ctx, key, strlen(key), EVP_md5(), NULL);
    HMAC_Update(&ctx, (unsigned char*)&plaintext, strlen(plaintext));
    HMAC_Final(&ctx, result, &len);
    HMAC_CTX_cleanup(&ctx);

    printf("Hashed string: ");

    for (int i = 0; i != len; i++)
        printf("%02x", (unsigned int)result[i]);

    printf("\n");

    free(result);

    return 0;
}

