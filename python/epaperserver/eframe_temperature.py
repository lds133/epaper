#!/usr/bin/python
# -*- coding: utf-8 -*-

from eframe_base import EFramePlugin
from openweathermap import WeatherInfo,OpenWeatherMap
import datetime
from sunrise import sun

from PIL import Image,ImageDraw,ImageFont
import random









class EFrameTemperature(EFramePlugin):

    RIGHTARROW = chr(8594)


    FORECAST_HOURS = 8

    OWP2METEOCOND = {
                        200	:  "Z"  ,	# thunderstorm with light rain	
                        201	:  "Z"  ,	# thunderstorm with rain	 
                        202	:  "&"  ,	# thunderstorm with heavy rain	
                        210	:  "Z"  ,	# light thunderstorm	 
                        211	:  "0"  ,	# thunderstorm	 
                        212	:  "6"  ,	# heavy thunderstorm	 
                        221	:  "6"  ,	# ragged thunderstorm	 
                        230	:  "0"  ,	# thunderstorm with light drizzle	
                        231	:  "0"  ,	# thunderstorm with drizzle	
                        232	:  "&"  ,	# thunderstorm with heavy drizzle

                        300	:  "L"  ,   # light intensity drizzle	
                        301	:  "L"  ,   # drizzle	
                        302	:  "R"  ,   # heavy intensity drizzle	 
                        310	:  "R"  ,   # light intensity drizzle rain	 
                        311	:  "R"  ,   # drizzle rain	 
                        312	:  "R"  ,   # heavy intensity drizzle rain	
                        313	:  "R"  ,   # shower rain and drizzle	 
                        314	:  "R"  ,   # heavy shower rain and drizzle	 
                        321	:  "R"  ,   # shower drizzle

                        500	:  "Q"  ,   # light rain	 
                        501	:  "Q"  ,   # moderate rain	 
                        502	:  "R"  ,   # heavy intensity rain	 
                        503	:  "R"  ,   # very heavy rain	 
                        504	:  "8"  ,   # extreme rain	 
                        511	:  "X"  ,   # freezing rain	
                        520	:  "R"  ,   # light intensity shower rain
                        521	:  "R"  ,   # shower rain	 
                        522	:  "8"  ,   # heavy intensity shower rain	
                        531	:  "8"  ,   # ragged shower rain	

                        600	:  "V"  ,   # light snow	
                        601	:  "U"  ,   # Snow	
                        602	:  "W"  ,   # Heavy snow	
                        611	:  "X"  ,   # Sleet	 
                        612	:  "X"  ,   # Light shower sleet	
                        613	:  "X"  ,   # Shower sleet	 
                        615	:  "X"  ,   # Light rain and snow	
                        616	:  "X"  ,   # Rain and snow	 
                        620	:  "W"  ,   # Light shower snow	 
                        621	:  "#"  ,   # Shower snow	
                        622	:  "#"  ,   # Heavy shower snow	 


                        701 :  "M"  ,   # Mist	
                        711 :  "M"  ,   # Smoke	
                        721 :  "M"  ,   # Haze	
                        731 :  "M"  ,   # Dust	sand/ dust whirls	
                        741 :  "M"  ,   # Fog	f
                        751 :  "M"  ,   # Sand	
                        761 :  "M"  ,   # Dust	
                        762 :  "M"  ,   # volcanic ash	 
                        771 :  "E"  ,   # Squall	
                        781 :  "F"  ,   # Tornado	


                        800 :  "B"  ,   # clear sky

                        801	:  "H"  ,   # few clouds: 11-25%	
                        802	:  "N"  ,   # scattered clouds: 25-50%	 
                        803	:  "Y"  ,   # broken clouds: 51-84%	 
                        804	:  "%"  ,   # overcast clouds: 85-100%	
}



    def __init__(self,openwathermap_object):
        self.w = openwathermap_object


        fontfile = '../pic/arial.ttf'
        mfontfile = '../pic/meteocons.ttf'


        self.font_arrow = ImageFont.truetype(fontfile, 50)
        self.font_tiny = ImageFont.truetype(fontfile, 70)
        self.font_small = ImageFont.truetype(fontfile, 100)
        self.font_m = ImageFont.truetype(mfontfile, 100)

 
    
    def Print(self,x,y,w,h,text,font):
        ww, hh = self.drawblack.textsize(text,font = font)
        self.drawblack.text((x+(w-ww)/2, y), text, font = font, fill = 0)



    def DrawWather(self,forecast,x,y,w,h):

        forecast.Print()
        
        t = int( round(forecast.temp) )


        if (t>0):
            tstr = "+"
        else:
            tstr = ""


        tstr = tstr + str(t)
        self.Print(x,y,w,h,tstr,self.font_small)



        if forecast.id in self.OWP2METEOCOND:
            idchar = self.OWP2METEOCOND[forecast.id]
        else:
            idchar = ")"
            
        y+=110
        self.Print(x,y,w,h,idchar,self.font_m)



    def Paint(self, xposition, yposition, HEIGHT, WIDTH, options=None):
        self.drawblack = ImageDraw.Draw(self.bimg)
        self.drawred = ImageDraw.Draw(self.rimg)

        x = xposition
        y = yposition

        f0 = self.w.GetCurr()
        f1 = self.w.Get(datetime.datetime.now()+datetime.timedelta(hours=self.FORECAST_HOURS))

        w = HEIGHT/2
        h = 0

        self.DrawWather(f0,x,y,w,h)
        x+=w
        self.DrawWather(f1,x,y,w,h)


        y+=90

        ww, hh = self.drawblack.textsize(self.RIGHTARROW,font = self.font_arrow)
        self.drawblack.text((x-ww/2, y), self.RIGHTARROW, font = self.font_arrow, fill = 0)

        

        



if __name__ == "__main__":

    import epd7in5b_sock as epd7in5b
    from PIL import Image,ImageDraw,ImageFont
    import PIL.ImageOps 

    HOST = "127.0.0.1"
    #HOST = "192.168.0.30"
    epd = epd7in5b.EPD(HOST)


    print("Image size %i,%i" % (epd7in5b.EPD_HEIGHT,epd7in5b.EPD_WIDTH))

    HBlackImage = Image.new('1', ( epd7in5b.EPD_HEIGHT,epd7in5b.EPD_WIDTH), 255)  
    HRedImage = Image.new('1', (epd7in5b.EPD_HEIGHT,epd7in5b.EPD_WIDTH), 255)  
    
    w = OpenWeatherMap()
    w.FromAuto()


    t = EFrameTemperature(w)
    t.SetPaper( HBlackImage, HRedImage)

    t.Paint( 0,0,epd7in5b.EPD_HEIGHT, epd7in5b.EPD_WIDTH, None)



    HBlackImage = HBlackImage.transpose(Image.ROTATE_270)
    HRedImage = HRedImage.transpose(Image.ROTATE_270)
        
        
    print("Init...")
    epd.init()
    print("Display...")
    epd.display(epd.getbuffer(HBlackImage), epd.getbuffer(HRedImage))
    print("Sleep...")
    epd.sleep()

