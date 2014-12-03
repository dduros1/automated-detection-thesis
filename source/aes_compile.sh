#!/bin/bash

compiler=(gcc) # clang)
pos_ind=(fpic fno-pic)
opt=(O O0 O1 O2 O3 Os Ofast Og)
#Compile with gcc
for i in "${pos_ind[@]}"
do
    for j in "${opt[@]}"
    do
        for k in "${compiler[@]}"
        do
            $k -Wall -Wextra -$i -$j -ggdb -o binaries/aestest\_$k\_$i\_$j aestest.c -lcrypto &>compile_results.txt
        done
    done
done

#Compile with clang


