#include "utils.h"

char itoa_buf[8] = "\0\0\0\0\0\0\0\0";
char * itoa(int16_t x) {
    // buf is at least char[8];
    uint8_t i = 6;
    do {
        itoa_buf[i--] = (x % 10) + '0';
        x /= 10;
    } while(x);

    // Must immediately use this.
    return itoa_buf + i + 1;
}

char subset_buf[8];
uint8_t is_subset(char * a, char * b) {
    char *i, *j;
    strcpy(subset_buf, b);
    for(i = a; *i; i ++) {
        for(j = subset_buf; *j; j++) {
            if (*j == *i) {
                *j = ' ';
                goto found;
            }
        }
        return 0;
        found: ;
    }
    return 1;
}
