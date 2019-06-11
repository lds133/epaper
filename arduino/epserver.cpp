#include "epserver.h"

#define PRINT(A) Serial.print(A)
#define PRINTLN(A) Serial.println(A)
#define PRINTPKT(A) Serial.print(A);Serial.println(_packetsize);


EPServer::EPServer(MyEpd* epd)
{
   _epd = epd;
   Reset();
}

EPServer::~EPServer(void)
{}


void EPServer::Reset()
{
    PRINTLN("> PACKET Reset");
    _state = STATE_HEADER;
    _stateindex = 0;
    _packetsize = 0;
    _packetid = 0;
    _isdrawenabled = false;
}

void EPServer::NewPacket()
{
    if (_packetid == PACKET_START)
    {   PRINTPKT("> PACKET_START ");  
        _epd->PicStart();
        return;
    }
    
    if (_packetid == PACKET_CONTINUE)
    {   PRINTPKT("> PACKET_CONTINUE ");
        _isdrawenabled = true;
        return;
    }
    
    if (_packetid == PACKET_STOP)
    {   PRINTPKT("> PACKET_STOP "); 
        _epd->PicStop();
        _isdrawenabled = true;

        return;
    }
    
    if (_packetid == PACKET_CLEAR)
    {   PRINTPKT("> PACKET_CLEAR ");   
        _epd->PicReset();
        _isdrawenabled = false;
        return;
    }
    
    if (_packetid == PACKET_SLEEP)
    {   PRINTPKT("> PACKET_SLEEP ");    
        _epd->PicSleep();
        _isdrawenabled = false;
        return;
    }

    PRINT("Warning: Wrong packet id ");
    PRINTLN(_packetid);
    _isdrawenabled = false;
  
}

void EPServer::ProcessByte(unsigned char b)
{

    if (_state == STATE_HEADER)
    {
        ((unsigned char*)&_packetsize)[_stateindex] = b;
        _stateindex++;
        if (_stateindex==4)
        {   _stateindex = 0;
            _state = STATE_ID;
        }
        return;
    }
    
    if (_state == STATE_ID)
    {
        _packetid = b;
        NewPacket();
        _state = STATE_DATA;
        _stateindex = 1;
        return;
    }

    
    if (_state == STATE_DATA)
    {   _epd->PicData( b );
        _stateindex++;
        if (_stateindex>=_packetsize)
            Reset();
        return;
    }
        
    if (_state == STATE_NONE)
    {   _stateindex++;
        if (_stateindex>=_packetsize)
            Reset();
    }
            
    PRINT("Error: State mashine broken");
    Reset();

}
        
