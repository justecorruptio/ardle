#include "jaylib.h"
#include "words.h"

Jaylib jay;

void setup() {
    jay.boot();
    jay.invert(1);
    jay.clear();

}

Words words;

int i = 0;
void loop() {
    //if(!jay.nextFrame()) return;

    jay.pollButtons();
    jay.clear();

    //if(jay.justPressed(A_BUTTON))
    if (words.phase != PHASE_END)
        words.next();

    jay.largePrint(10, (i++ % 8) * 8, words.buff, 1);

    jay.display();
}

// vim:syntax=c
