#!/bin/bash

algorithms=(\3des\_cbc \3des\_ofb \3des\_cfb aes hmac\_md5 hmac\_sha1 md5 rsa sha1 rc4)
compiler=(gcc) # clang)
pos_ind=(fpic fno-pic)
opt=(O O0 O1 O2 O3 Os Ofast Og)
#Compile with gcc
for alg in "${algorithms[@]}"
do
    for i in "${pos_ind[@]}"
    do
        for j in "${opt[@]}"
        do
            for k in "${compiler[@]}"
            do
                echo $alg
$k -Wall -Wextra -$i -$j -ggdb -o ../binaries/$alg-test\_$k\_$i\_$j openssl\_$alg.c -lcrypto &>compile_results.txt
            done
        done
    done
done

#Compile with clang


