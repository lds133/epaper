#ifndef MYEPDIF_H
#define MYEPDIF_H

#include <arduino.h>

// Pin definition
#define RST_PIN       16//  8
#define DC_PIN        5//  9
#define CS_PIN        15//  10
#define BUSY_PIN      4//  7

class MyEpdIf {
public:
    MyEpdIf(void);
    ~MyEpdIf(void);

    static int  IfInit(void);
    static void DigitalWrite(int pin, int value); 
    static int  DigitalRead(int pin);
    static void DelayMs(unsigned int delaytime);
    static void SpiTransfer(unsigned char data);
};

#endif
