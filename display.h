#pragma once

#include "jaylib.h"

#define STYLE_BLANK 0
#define STYLE_GRAY 1
#define STYLE_YELLOW 2
#define STYLE_GREEN 3



class Display {

    public:
    void drawTile(Jaylib &jay, uint8_t row, uint8_t col, char letter, uint8_t style);
};
