#include "display.h"

void Display::drawTile(Jaylib &jay, uint8_t row, uint8_t col, char letter, uint8_t style) {
    uint8_t x = 3 + col * 12;
    uint8_t y = 3 + row * 12;
    if(style == STYLE_YELLOW) {
        jay.drawLargeCharBand(x, y, 7 * (':' - 48), 11);
        jay.drawLargeCharBand(x + 8, y, 7 * (':' - 48) + 11, 11);
    } else if (style == STYLE_GREEN) {
        jay.drawLargeCharBand(x, y, 7 * (':' - 48) + 22, 11);
        jay.drawLargeCharBand(x + 4, y, 7 * (':' - 48) + 22, 11);
    }

    jay.drawLargeCharBand(x + 3, y + 2, 7 * (letter - 48), 7, style == STYLE_YELLOW);
}
