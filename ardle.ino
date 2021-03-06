#include "jaylib.h"
#include "words.h"
#include "display.h"

Jaylib jay;
Display display;

Words words;

void setup() {
    jay.boot();
    //jay.invert(1);
    jay.clear();
}


void loop() {
    if(!jay.nextFrame()) return;

    jay.pollButtons();
    jay.clear();


    if(jay.justReleased(A_BUTTON))
    while (words.phase != PHASE_END) {
        words.next();
        if(words.flags & 4) break;
        //break;
    }

    jay.largePrint(10, 90, words.buff);

    jay.smallPrint(3, 105, "QWERTYUIOP", 1);
    jay.smallPrint(6, 113, "ASDFGHJKL", 1);
    jay.smallPrint(9, 121,"ZXCVBNM[", 1);

    for(uint8_t i= 0; i < 6; i++) {
        for(uint8_t j= 0; j < 5; j++) {
            //jay.drawLargeCharBand(3 + j * 12, 3 + i * 12, 7 * (':' - 48), 11);
            //jay.drawLargeCharBand(3 + j * 12 + 8, 3 + i * 12, 7 * (':' - 48) + 11, 11);
            //jay.largePrint(3 + j * 12 + 3, 3 + i * 12 + 2, "A", 1);

            display.drawTile(jay, i, j, 'B', 2);
        }
    }

    jay.display();
}

// vim:syntax=c
