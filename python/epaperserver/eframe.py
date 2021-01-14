#!/usr/bin/python
# -*- coding: utf-8 -*-

import epd7in5b_sock as epd7in5b
#import epd7in5b

from PIL import Image,ImageDraw,ImageFont

from openweathermap import WeatherInfo,OpenWeatherMap
from eframe_base     import EFramePlugin
from eframe_calendar4 import EFrameCalendar
from eframe_weather2  import EFrameWeather,EFrameClock
from eframe_temperature import EFrameTemperature





def MakeEFramePicture(epaperserverip="127.0.0.1"):


    #epd = epd7in5b.EPD()
    epd = epd7in5b.EPD(epaperserverip)

    #epd.init()
    #print("Clear...")
    #epd.Clear(0xFF)
    #epd.sleep()

    w = OpenWeatherMap("/var/ram")
    w.FromAuto()



    plugins = [ ( EFrameCalendar(), 0 , 0   ), 
                ( EFrameTemperature(w), 0 , 250   ), 
                ( EFrameWeather(w),  0 , 565 ),
                ( EFrameClock(),  366,5),#366, 640),
              ]


    #HBlackImage = Image.open('..\pic\cat.bmp')
    #HBlackImage = Image.open('..\pic\kettle.bmp')
    #HBlackImage = Image.open('..\pic\jun1_1979_black.bmp')
    #HRedImage = Image.open('..\pic\jun1_1979_red.bmp')


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
    #MakeEFramePicture("192.168.0.30")
    MakeEFramePicture()