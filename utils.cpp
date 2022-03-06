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
