#ifndef JAYLIB_H
#define JAYLIB_H

#include <Arduboy2.h>

class Jaylib: public Arduboy2Base {
    public:
    void drawBand(uint8_t x, uint8_t y, const uint8_t * sprite, uint8_t cols, uint8_t color = 1);

    void smallPrint(uint8_t x, uint8_t y, const uint8_t * str, uint8_t color = 1);
    void largePrint(uint8_t x, uint8_t y, const uint8_t * str, uint8_t color = 1);

    void drawFastVLine(uint8_t x, uint8_t y, uint8_t h, uint8_t color = 1);
    void drawFastHLine(uint8_t x, uint8_t y, uint8_t w, uint8_t color = 1);

    void drawPixel(int16_t x, int16_t y, uint8_t color = WHITE);
    void drawLargeCharBand(int16_t x, int16_t y, uint8_t c, uint8_t l, uint8_t color=WHITE);
};

#endif
