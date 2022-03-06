#include "words.h"
#include "generated_data/compresssed_data.h"

Words::Words() {
    phase = 1;
    idx = 0;
    pathIdx = 0;
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
    if(phase == PHASE_SINGLE) {
        do {
            b = pgm_read_byte(SINGLE_STREAM + idx++);
            delta = (delta << 7) | (b & 0x7f);
        } while ((b & 0x80) == 0);

        value += delta + 1;
        decodeWord();
        if(idx >= SINGLE_STREAM_LENGTH) {
            phase = PHASE_PATH;
            idx = 0;
            value = 0;
        }
    } else if(phase == PHASE_PATH) {
        do {
            b = pgm_read_byte(PATH_STREAM + idx++);
            delta = (delta << 7) | (b & 0x7f);
        } while ((b & 0x80) == 0);
        value += delta + 1;
        decodeWord();
        phase = PHASE_STEP;
    } else if(phase == PHASE_STEP) {
        b = pgm_read_byte(PATH_STEPS + pathIdx++);
        uint8_t pos = (b & 0x7f) / 25;
        uint8_t rot = ((b & 0x7f) % 25) + 1;
        uint8_t c = (buff[pos] - 'A' + rot) % 26 + 'A';
        buff[pos] = c;
        if(b & 0x80) {
            if(idx >= PATH_STREAM_LENGTH) phase = PHASE_END;
            else phase = PHASE_PATH;
        }
    }
}
