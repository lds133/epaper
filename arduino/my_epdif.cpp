

#include "my_epdif.h"
#include <spi.h>

MyEpdIf::MyEpdIf() {
};

MyEpdIf::~MyEpdIf() {
};

void MyEpdIf::DigitalWrite(int pin, int value) {
    digitalWrite(pin, value);
}

int MyEpdIf::DigitalRead(int pin) {
    return digitalRead(pin);
}

void MyEpdIf::DelayMs(unsigned int delaytime) {
    delay(delaytime);
}

void MyEpdIf::SpiTransfer(unsigned char data) {
    digitalWrite(CS_PIN, LOW);
    SPI.transfer(data);
    digitalWrite(CS_PIN, HIGH);
}

int MyEpdIf::IfInit(void) {
    pinMode(CS_PIN, OUTPUT);
    pinMode(RST_PIN, OUTPUT);
    pinMode(DC_PIN, OUTPUT);
    pinMode(BUSY_PIN, INPUT); 
    SPI.beginTransaction(SPISettings(2000000, MSBFIRST, SPI_MODE0));
    SPI.begin();
    return 0;
}

