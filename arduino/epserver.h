#ifndef EPSERVER_H
#define EPSERVER_H

#include "my_epd7in5b.h"

// 00 00 00 00 : size (not included this 4 bytes)
// 00          : id
// 00 00 ...   : data 

//got from  my_epd7in5b.h
//#define EPD_WIDTH       = 640
//#define EPD_HEIGHT      = 384

#define PACKET_NONE      0
#define PACKET_START     1
#define PACKET_CONTINUE  2
#define PACKET_STOP      3
#define PACKET_CLEAR     4
#define PACKET_SLEEP     5

#define STATE_NONE       0
#define STATE_HEADER     1
#define STATE_ID         2
#define STATE_DATA       3



class EPServer 
{
  public:
    EPServer(MyEpd* epd);
    ~EPServer(void);

    void ProcessByte(unsigned char b);
    void Reset();


  private:
    MyEpd* _epd;
    int _state;
    unsigned int _stateindex;
    unsigned _packetsize;
    unsigned _packetid;
    bool _isdrawenabled;    
    void NewPacket();

};

#endif



