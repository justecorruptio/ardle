#ifndef JAYLIB_H
#define JAYLIB_H

#include <Arduboy2.h>
#include <avr/power.h>

#include "jay_sprites.h"

class Jaylib: public Arduboy2Base {
    public:
    void drawBand(uint8_t x, uint8_t y, const uint8_t * sprite, uint8_t cols);

    void smallPrint(uint8_t x, uint8_t y, const uint8_t * str);
    void largePrint(uint8_t x, uint8_t y, const uint8_t * str, uint8_t kern = 1);

    void drawFastVLine(uint8_t x, uint8_t y, uint8_t h);
    void drawFastHLine(uint8_t x, uint8_t y, uint8_t w);
};

#endif
