#include "jaylib.h"
#include "words.h"

Jaylib jay;

Words words;

void setup() {
    jay.boot();
    jay.invert(1);
    jay.clear();
}


void loop() {
    if(!jay.nextFrame()) return;

    jay.pollButtons();
    jay.clear();


    if(jay.justPressed(A_BUTTON))
    while (words.phase != PHASE_END) {
        words.next();
        //if(words.answerSteps == 0) break;
    }

    jay.largePrint(10, 30, words.buff, 1);

    jay.largePrint(1, 1, "ABCDEFGHIJ", 1);
    jay.largePrint(1, 9, "KLMNOPQRST", 1);
    jay.largePrint(1, 17,"UVWXYZ", 1);
    jay.largePrint(1, 25,"01234", 1);
    jay.largePrint(1, 33,"56789:", 1);

    jay.display();
}

// vim:syntax=c
