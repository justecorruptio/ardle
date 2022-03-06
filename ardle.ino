#include "jaylib.h"
#include "generated_data/compresssed_data.h"

Jaylib jay;

void setup() {
    jay.boot();
    jay.invert(1);
    jay.clear();

}

void loop() {
    if(!jay.nextFrame()) return;

    jay.pollButtons();
    jay.clear();

    jay.largePrint(10, 10, "HELLO WORLD", 1);
    pgm_read_byte(SINGLE_STREAM);
    pgm_read_byte(PATH_STREAM);
    pgm_read_byte(PATH_STEPS);
    pgm_read_byte(ANSWER_STREAM);

    jay.display();
}

// vim:syntax=c
