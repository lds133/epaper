#include <SPI.h>
#include "my_epd7in5b.h"
#include "ESP8266WiFi.h"
#include "epserver.h"


#define PIN_BLUETOP       LED_BUILTIN
#define PIN_GREEN         11




#include "leds.h"


#define PRINTESPINFO(A)  Serial.print(#A ": ");Serial.println(ESP.get##A()  ); 
 
const char* ssid = "XXXXXXXX";
const char* password = "XXXXXXXXX";
const int port = 5555;
 
WiFiServer _wifiserver(port);
MyEpd _epd;
EPServer _serv(&_epd);



/*
RST       16
DC        5
CS        15
BUSY      4
SCK       14
MISO      12
MOSI      13
*/


bool _isnolight = false;
unsigned long _lastupdatetime=0;
unsigned long _lastsleeptime=0;

const unsigned long SLEEPTIMEOUT = 10*60*1000;// 10mins
const unsigned long CLEARTIMEOUT = 240*60*1000;// 4 hours


void eppaperkeeper_reset()
{
    unsigned long t = millis();
    _lastupdatetime=t;
    _lastsleeptime=t;
}

void eppaperkeeper()
{
    unsigned long t = millis();
  
    if ((t - _lastupdatetime)>CLEARTIMEOUT)
    {   _lastsleeptime=t;
        _lastupdatetime = t;
        Serial.println("Clean Timeout...");
        _epd.PicReset();
        Serial.println("Clean done");   
    }  

    if ((t - _lastsleeptime)>SLEEPTIMEOUT)
    {   _lastsleeptime =t;
        Serial.println("Sleep Timeout...");
        _epd.PicSleep();
    }    
}





void do_staff()
{
    unsigned long t = millis();
    led_loop(t,_isnolight);
    yield();// avoid ESP WDT reset

}






void safedelay(unsigned long ms)
{
  unsigned long waittimer = millis();
  while(true)
  {   unsigned long t = millis();
      if (t-waittimer>ms)
          break;
      do_staff();
      delay(1);  

  }
}

void esp_reset()
{
    Serial.println("ESP RESERT IN 30 SEC !!!");
    safedelay(30000);
    ESP.reset();
}



void WaitForWiFi()
{
    int fuse=0;
    while (WiFi.status() != WL_CONNECTED) 
    {
      fuse++;
      safedelay(500);
      Serial.print(".");
      if (fuse>1800)//15mins
            esp_reset();
    }
    Serial.println();

}


void setup() 
{
  
    Serial.begin(115200);

    Serial.println("* EPaper Server * (c) June 2019\r\n");

    PRINTESPINFO(ChipId);
    PRINTESPINFO(FlashChipSize);
    PRINTESPINFO(FreeHeap);
    PRINTESPINFO(FreeSketchSpace);
    PRINTESPINFO(SketchSize);
    PRINTESPINFO(FlashChipId);
    PRINTESPINFO(SdkVersion);
    PRINTESPINFO(FlashChipRealSize);
    PRINTESPINFO(CpuFreqMHz);
    PRINTESPINFO(FlashChipSpeed);

    led_setup();

    Serial.println();

    led_set(LED_BLUE2,LED_BLINK);
  
    _epd.SetDoStaffFuncftion(&do_staff);

    Serial.println("Clean...");
    _epd.PicReset();
    Serial.println("Clean done");


    WiFi.setSleepMode(WIFI_NONE_SLEEP);
    WiFi.persistent(false);
    WiFi.softAPdisconnect(true);
    WiFi.begin(ssid, password);
 
    led_set(LED_BLUE2,LED_ON);
    Serial.print("Connecting ");
    Serial.print(ssid);
    Serial.print(" ");
    WaitForWiFi();
    Serial.println();

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
  
    byte mac[6];
    WiFi.macAddress(mac);
    Serial.print("MAC: ");
    Serial.print(mac[0],HEX);
    Serial.print(":");
    Serial.print(mac[1],HEX);
    Serial.print(":");
    Serial.print(mac[2],HEX);
    Serial.print(":");
    Serial.print(mac[3],HEX);
    Serial.print(":");
    Serial.print(mac[4],HEX);
    Serial.print(":");
    Serial.println(mac[5],HEX);


    _wifiserver.begin();
    Serial.print("Server started. status =");
    Serial.println(_wifiserver.status());

    
    led_set(LED_BLUE2,LED_BLINKLO); 


    eppaperkeeper_reset();

    //todo: enable blink by sending packet
    _isnolight = true;

}

void loop() 
{

    if (WiFi.status() != WL_CONNECTED) 
    {
        esp_reset();
    }
    
  
    WiFiClient client = _wifiserver.available();
   
    if (client) 
    {   

       
        if(client.connected())
        {  Serial.println("Client Connected");
           led_set(LED_BLUE2,LED_BLINKHI); 
        }
          
        _serv.Reset();

        while (client.connected()) 
        {   
            unsigned int n = 0;
            while (client.available()>0) 
            {   char c = client.read();
                n++;
                _serv.ProcessByte((unsigned char)c);

            } 
            if (n!=0)
            {   Serial.print(n);
                Serial.println(" bytes processed");
            }
            safedelay(1);

            eppaperkeeper();
        }

        _epd.PicSleep();
        client.stop();
        Serial.println("Client disconnected");
        led_set(LED_BLUE2,LED_BLINKLO);
        


        eppaperkeeper_reset();
    }

    safedelay(10);
    eppaperkeeper();

}
