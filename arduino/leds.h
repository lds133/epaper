
#define LED_OFF        0
#define LED_ON         1
#define LED_BLINK      2 
#define LED_BLINKLO    3 
#define LED_BLINKHI    4 


int  _ledpins[] =  {PIN_BLUETOP};//,PIN_BLUE,PIN_RED,PIN_GREEN};
int  _ledhi[]   =  {LOW};//,HIGH,HIGH,HIGH};
int  _ledlo[]   =  {HIGH};//,LOW,LOW,LOW};
int _ledmode[] =  {LED_OFF};//,LED_OFF,LED_OFF,LED_OFF};


#define LED_BLUE2   0
//#define LED_BLUE    1
//#define LED_RED     2
//#define LED_GREEN   3
#define LED_MAX     (sizeof(_ledpins)/sizeof(int))

#define LED_FLASHPERIOD   250
#define LED_FLASCYCLEMAX  4

void led_set(int i,int ledmode)
{
    _ledmode[i] = ledmode;
    
    if (ledmode==LED_OFF)
    {   digitalWrite(_ledpins[i],_ledlo[i]);
        return;
    } 
    
    if (ledmode==LED_ON)
    {   digitalWrite(_ledpins[i],_ledhi[i]); 
        return;
    }

    //digitalWrite(_ledpins[i],_ledlo[i]);
    return;    
}

void led_setup()
{
    for(int i=0;i<LED_MAX;i++)
    {   pinMode(_ledpins[i], OUTPUT);
        led_set(i,LED_OFF);
    }
}




void led_animation(int i,int a,bool isnolight)
{
    if (isnolight)
    {
        digitalWrite(_ledpins[i], _ledlo[i]);
        return;  
    }
  
    if (_ledmode[i]==LED_BLINK)
    {
        digitalWrite(_ledpins[i],((a==0)||(a==1)) ? _ledhi[i] : _ledlo[i]);
        return;
    }  

    if (_ledmode[i]==LED_BLINKLO)
    {
        digitalWrite(_ledpins[i],(a==0) ? _ledhi[i] : _ledlo[i]);
        return;
    }  

    if (_ledmode[i]==LED_BLINKHI)
    {
        digitalWrite(_ledpins[i],((a==0)||(a==2)) ? _ledhi[i] : _ledlo[i]);
        return;
    }  

}


unsigned long _flashtime=0;
unsigned long _flashanistage=0;

void led_loop(unsigned long now,bool isnolight)
{
    
  
    if (now-_flashtime>LED_FLASHPERIOD)
    {

        for(int i=0;i<LED_MAX;i++)
            led_animation(i,_flashanistage,isnolight);
        _flashanistage++;
        if (_flashanistage>=LED_FLASCYCLEMAX)
            _flashanistage=0;
        _flashtime=now;
    }

    
}

