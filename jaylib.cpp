#include "jaylib.h"
#include "utils.h"
#include "jay_horiz_sprites.h"

void Jaylib::drawBand(uint8_t x, uint8_t y, const uint8_t * sprite, uint8_t cols, uint8_t color) {
    uint16_t s;
    uint16_t p = (y >> 3) * WIDTH + cols + x - 1;

    for(; cols --; p --) {
        s = pgm_read_byte(sprite + cols) << (y & 0x7);

        if(color) {
            sBuffer[p] |= s;
            sBuffer[p + WIDTH] |= s >> 8;
        } else {
            sBuffer[p] &= ~s;
            sBuffer[p + WIDTH] &= ~s >> 8;
        }
    }
}

void Jaylib::smallPrint(uint8_t x, uint8_t y, const uint8_t * str) {
    char c;
    for(;c = *str ++;) {
        c -= 32;
        drawBand(x, y, PRINTABLE_CHARS + 3 * c, 3);
        x += 4;
    }
}

void Jaylib::largePrint(uint8_t x, uint8_t y, const uint8_t * str, uint8_t color) {
    char c;
    for(;c = *str ++;) {
        c -= HORIZ_OFFSET;
        drawBand(128 - y - 7, x, HORIZ_LARGE_CHARS + 7 * c, 7, color);
        x += 6;
    }
}

void Jaylib::drawFastVLine(uint8_t x, uint8_t y, uint8_t h, uint8_t color) {
    uint8_t i;
    for(i = h; i --;)
        drawPixel(127 - y - i, x, color);
}

void Jaylib::drawFastHLine(uint8_t x, uint8_t y, uint8_t w, uint8_t color) {
    uint8_t i;
    for(i = w; i --;)
        drawPixel(127 - y, x + i, color);
}

void Jaylib::drawPixel(int16_t x, int16_t y, uint8_t color) {
    // Use the tip of the L to draw a dot.
    drawBand(x, y, HORIZ_LARGE_CHARS + 7 * ('L' - HORIZ_OFFSET) + 1, 1, color);
}
