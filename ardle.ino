#include "jaylib.h"
#include "words.h"

Jaylib jay;

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

    jay.largePrint(10, 100, words.buff);

    /*
    jay.largePrint(1, 1, "ABCDEFGHIJ", 1);
    jay.largePrint(1, 9, "KLMNOPQRST", 1);
    jay.largePrint(1, 17,"UVWXYZ", 1);
    jay.largePrint(1, 25,"01234", 1);
    jay.largePrint(1, 33,"56789:", 1);
    */
    jay.smallPrint(3, 105, "QWERTYUIOP", 1);
    jay.smallPrint(6, 113, "ASDFGHJKL", 1);
    jay.smallPrint(9, 121,"ZXCVBNM[", 1);


    for(uint8_t i= 0; i < 6; i++) {
        for(uint8_t j= 0; j < 5; j++) {
            jay.drawFastHLine(3 + j * 12, 3 + i * 12, 11);
            jay.drawFastHLine(3 + j * 12, 13 + i * 12, 11);
            jay.drawFastVLine(3 + j * 12, 3 + i * 12, 11);
            jay.drawFastVLine(13 + j * 12, 3 + i * 12, 11);

            jay.largePrint(3 + j * 12 + 3, 3 + i * 12 + 2, "A", 1);
        }
    }

    jay.display();
}

// vim:syntax=c
