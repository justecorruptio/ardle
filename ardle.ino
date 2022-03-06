#include "jaylib.h"
#include "words.h"

Jaylib jay;

void setup() {
    jay.boot();
    jay.invert(1);
    jay.clear();

}

Words words;

void loop() {
    if(!jay.nextFrame()) return;

    jay.pollButtons();
    jay.clear();

    jay.largePrint(10, 10, "HELLO WORLD", 1);
    pgm_read_byte(SINGLE_STREAM);
    pgm_read_byte(PATH_STREAM);
    pgm_read_byte(PATH_STEPS);
    pgm_read_byte(ANSWER_STREAM);

    if(jay.justPressed(A_BUTTON)) words.next();

    jay.largePrint(10, 30, words.buff, 1);

    jay.display();
}

// vim:syntax=c
