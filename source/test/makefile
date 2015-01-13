CC = gcc
CFLAGS = -Wall
OBJECTS=aes arcfour blowfish des md2 md5 rot-13 sha1
OBJECTPATH=../../binaries/test/crypto/

.PHONY: all move clean

all: $(OBJECTS) move

clean:
	rm -rf $(OBJECTS)

aes: aes_test.c aes.c
	$(CC) $(CFLAGS) -o aes aes_test.c aes.c

arcfour: arcfour_test.c arcfour.c
	$(CC) $(CFLAGS) -o arcfour arcfour_test.c arcfour.c

blowfish: blowfish_test.c blowfish.c
	$(CC) $(CFLAGS) -o blowfish blowfish_test.c blowfish.c

des: des_test.c des.c
	$(CC) $(CFLAGS) -o des des_test.c des.c

md2: md2_test.c md2.c
	$(CC) $(CFLAGS) -o md2 md2_test.c md2.c

md5: md5_test.c md5.c
	$(CC) $(CFLAGS) -o md5 md5_test.c md5.c

rot-13: rot-13_test.c rot-13.c
	$(CC) $(CFLAGS) -o rot-13 rot-13_test.c rot-13.c

sha1: sha1_test.c sha1.c
	$(CC) $(CFLAGS) -o sha1 sha1_test.c sha1.c

move:           
	$(MV) $(OBJECTs) $(OBJECT_PATH)
