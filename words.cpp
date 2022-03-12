#include "words.h"
#include "generated_data/compresssed_data.h"

Words::Words() {
    phase = 0;
    idx = 0;
    pathIdx = 0;
    value = 0;
    buff[5] = '\0';
    counter = 0;
    flags = 0;
}

void Words::decodeWord() {
    for(uint8_t i = 0; i < 5; i++)
        buff[4 - i] = ((value >> (i * 5)) & 0x1f) + 'A';
}

void Words::walkStream(char* ptr) {
    uint32_t delta = 0;
    uint8_t b;
    do {
        b = pgm_read_byte(ptr + idx++);
        delta = (delta << 7) | (b & 0x7f);
    } while ((b & 0x80) == 0);
    value += delta + 1;
    decodeWord();
}

uint8_t Words::next() {
    /*
    if(answerSteps == 0) {
        uint32_t v = pgm_read_dword(ANSWER_STREAM + (answerIdx / 4 * 3));
        answerSteps = (v >> ((answerIdx % 4) * 6)) & 0x3f;
        answerIdx ++;
    }
    answerSteps --;
    */
    uint32_t v = pgm_read_dword(FLAGS_STREAM + (counter / 8 * 3));
    flags = (v >> ((counter % 8) * 3)) & 0x7;

    if(phase == PHASE_SINGLE) {
        walkStream(SINGLE_STREAM);
        if(idx >= SINGLE_STREAM_LENGTH)
            phase = PHASE_PATH, idx = value = 0;
    } else if(phase == PHASE_PATH) {
        walkStream(PATH_STREAM);
        phase = PHASE_STEP;
    } else if(phase == PHASE_STEP) {
        uint8_t b = pgm_read_byte(PATH_STEPS + pathIdx++);

        uint8_t rot = b & 0x7f, pos = 0;
        while(rot >= 25) rot -=25, pos ++;

        buff[pos] += rot + 1; if(buff[pos] > 'Z') buff[pos] -= 26;
        if(b & 0x80)
            phase = idx >= PATH_STREAM_LENGTH ? PHASE_END : PHASE_PATH;
    }

    counter += 1;
}
