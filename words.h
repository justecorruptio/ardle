#pragma once
#include "jaylib.h"
#include "generated_data/compresssed_data.h"

class Words {
    public:
    uint8_t phase;
    uint16_t idx;
    uint64_t value;
    uint8_t buff[8];
    uint8_t isAnswer;

    Words();
    uint8_t next();
    void decodeWord();
};
