#!/usr/bin/python
# -*- coding: utf-8 -*-

import epd7in5b_sock as epd7in5b
#import epd7in5b

from PIL import Image,ImageDraw,ImageFont

from eframe_base     import EFramePlugin
from eframe_calendar import EFrameCalendar
from eframe_weather  import EFrameWeather





def MakeEFramePicture(epaperserverip="127.0.0.1"):


    #epd = epd7in5b.EPD()
    epd = epd7in5b.EPD(epaperserverip)

    #epd.init()
    #print("Clear...")
    #epd.Clear(0xFF)
    #epd.sleep()


    plugins = [ ( EFrameCalendar(), 0 , 0   ), 
                ( EFrameWeather(),  0 , 570 ),
              ]






    HBlackImage = Image.new('1', ( epd7in5b.EPD_HEIGHT,epd7in5b.EPD_WIDTH), 255)  
    HRedImage = Image.new('1', (epd7in5b.EPD_HEIGHT,epd7in5b.EPD_WIDTH), 255)    

    for (p,x,y) in plugins:
        p.SetPaper( HBlackImage, HRedImage)
        p.Paint( x, y,epd7in5b.EPD_HEIGHT, epd7in5b.EPD_WIDTH, None)

    HBlackImage = HBlackImage.transpose(Image.ROTATE_270)
    HRedImage = HRedImage.transpose(Image.ROTATE_270)

    #try:

    print("EPD Init...")
    epd.init()
    print("EPD Display...")
    epd.display(epd.getbuffer(HBlackImage), epd.getbuffer(HRedImage))
    print("EPD Sleep...")
    epd.sleep()

    #except:
    #    print("EPD exception !!!")


if __name__ == "__main__":
    MakeEFramePicture()