#include "words.h"

Words::Words() {
    phase = 0;
    idx = 0;
    value = 0;
    buff[5] = '\0';
    isAnswer = 0;
}

void Words::decodeWord() {
    for(uint8_t i = 0; i < 5; i++)
        buff[4 - i] = ((value >> (i * 5)) & 0x1f) + 'A';
}

uint8_t Words::next() {
    uint64_t delta = 0;
    uint8_t b;
    if(phase == 0) {
        do {
            b = pgm_read_byte(SINGLE_STREAM + idx++);
            delta = (delta << 7) | (b & 0x7f);
        } while ((b & 0x80) == 0);

        value += delta + 1;
        decodeWord();
    }
}
