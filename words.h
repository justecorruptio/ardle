#pragma once
#include "jaylib.h"

#define PHASE_SINGLE 0
#define PHASE_PATH 1
#define PHASE_STEP 2
#define PHASE_END 3

class Words {
    public:
    uint8_t phase;
    uint16_t idx;
    uint16_t pathIdx;
    uint32_t value;
    uint8_t buff[6];

    uint8_t answerIdx;
    uint8_t answerSteps;

    Words();
    uint8_t next();

    private:
    void decodeWord();
    void walkStream(char* ptr);
};
