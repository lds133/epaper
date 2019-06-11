#include <stdlib.h>
#include "my_epd7in5b.h"


#define PRINT(A) Serial.print(A)
#define PRINTLN(A) Serial.println(A)


void MyEpd::SetDoStaffFuncftion(DoStaffFunc f)
{
    _fnc = f;
}

void MyEpd::SafeDelayMs(unsigned long n)
{
    if (_fnc==NULL)
    {
        DelayMs(n);
        return;
    }
    
    const unsigned long dn = 10;
    while(true)
    {
        if (n<dn)
        {   
            if (n!=0)
                DelayMs(n);
            break;
        }
        _fnc();
        DelayMs(dn);
        n-=dn;
        
    }
}




MyEpd::~MyEpd()
{
    _fnc = NULL; 
 }

MyEpd::MyEpd() {
    reset_pin = RST_PIN;
    dc_pin = DC_PIN;
    cs_pin = CS_PIN;
    busy_pin = BUSY_PIN;
    width = EPD_WIDTH;
    height = EPD_HEIGHT;
};

int MyEpd::Init(void) {
    
    
    
    if (IfInit() != 0) {
        return -1;
    }
    
    PRINTLN("$ Init");
       
    Reset();

    SendCommand(POWER_SETTING); 
    SendData(0x37);
    SendData(0x00);

    SendCommand(PANEL_SETTING);
    SendData(0xCF);
    SendData(0x08);
    
    SendCommand(BOOSTER_SOFT_START);
    SendData(0xc7);     
    SendData(0xcc);
    SendData(0x28);

    SendCommand(POWER_ON);
    WaitUntilIdle();

    SendCommand(PLL_CONTROL);
    SendData(0x3A);        

    SendCommand(TEMPERATURE_CALIBRATION);
    SendData(0x00);

    SendCommand(VCOM_AND_DATA_INTERVAL_SETTING);
    SendData(0x77);

    SendCommand(TCON_SETTING);
    SendData(0x22);

    SendCommand(TCON_RESOLUTION);
    SendData(0x02);     //source 640
    SendData(0x80);
    SendData(0x01);     //gate 384
    SendData(0x80);

    SendCommand(VCM_DC_SETTING);
    SendData(0x1E);      //decide by LUT file

    SendCommand(0xe5);           //FLASH MODE            
    SendData(0x03);  

    _isinsleepmode=false;

    return 0;
}

/**
 *  @brief: basic function for sending commands
 */
void MyEpd::SendCommand(unsigned char command) {
    DigitalWrite(dc_pin, LOW);
    SpiTransfer(command);
}

/**
 *  @brief: basic function for sending data
 */
void MyEpd::SendData(unsigned char data) 
{
    DigitalWrite(dc_pin, HIGH);
    SpiTransfer(data);
    yield();   
    
}

/**
 *  @brief: Wait until the busy_pin goes HIGH
 */
void MyEpd::WaitUntilIdle(void) 
{
#ifndef DEBUG   

    PRINTLN("$ Wait idle");
    while(DigitalRead(busy_pin) == 0) 
    {      //0: busy, 1: idle
        SafeDelayMs(100);
    }      
    PRINTLN("$ Idle");
    
#endif
    
}

/**
 *  @brief: module reset.
 *          often used to awaken the module in deep sleep,
 *          see Epd::Sleep();
 */
void MyEpd::Reset(void) {

    PRINTLN("$ Reset");
  
    DigitalWrite(reset_pin, LOW);                //module reset    
    SafeDelayMs(200);
    DigitalWrite(reset_pin, HIGH);
    SafeDelayMs(200);    
}

void MyEpd::Clean(void) {

    PRINTLN("$ Clean");
  
    SendCommand(DATA_START_TRANSMISSION_1);
    for (unsigned long i = 0; i < 122880; i++) 
        SendData(0x33); 
    SendCommand(DISPLAY_REFRESH);
    SafeDelayMs(100);
    WaitUntilIdle();
}


/**
 *  @brief: After this command is transmitted, the chip would enter the 
 *          deep-sleep mode to save power. 
 *          The deep sleep mode would return to standby by hardware reset. 
 *          The only one parameter is a check code, the command would be
 *          executed if check code = 0xA5. 
 *          You can use EPD_Reset() to awaken
 */
void MyEpd::Sleep(void) 
{
    PRINTLN("$ Sleep");
    
    SendCommand(POWER_OFF);
    WaitUntilIdle();
    SendCommand(DEEP_SLEEP);
    SendData(0xa5);
    _isinsleepmode = true;    


}





void MyEpd::PicStart()
{
    Init();
    SendCommand(DATA_START_TRANSMISSION_1);
    PRINTLN("$ Start transmission");
}

void MyEpd::PicData(unsigned char b)
{
   SendData(b);
}

void MyEpd::PicStop()
{
    PRINTLN("$ Refresh");
    SendCommand(DISPLAY_REFRESH);
    SafeDelayMs(100);
    WaitUntilIdle();
    Sleep();
}

void MyEpd::PicSleep()
{
    if (!_isinsleepmode)
       Sleep();
}

void MyEpd::PicReset()
{   
    Init();
    Clean();
    Sleep();
}



