#!/usr/bin/python
# -*- coding: utf-8 -*-

from eframe_base import EFramePlugin
from openweathermap import WeatherInfo,OpenWeatherMap
import datetime
from sunrise import sun

from PIL import Image,ImageDraw,ImageFont


class DrawWeather():

    YSTEP = 32
    XSTEP = 48
    RAIN100 = 4.0



    def __init__(self,bimg,rimg):

        self.bimg = bimg
        self.rimg = rimg
        self.dir = '../wicons/'
        self.ext = '.png'


    def Invert1(self,img):
        width, height = img.size
        i = Image.new('1', ( width,height), 1)  
        ip = i.load() 
        imgp = img.load()
        for x in range(width):   
            for y in range(height):
                if (imgp[x,y]!=0):
                    ip[x,y]=0
        return i


    def PutImg(self,name,index,x,y,isblack=True):
        imagepath = "%s%s_%02i%s" % (self.dir, name, index, self.ext)
        
        i = Image.open(imagepath).convert("1")
        width, height = i.size
        m = self.Invert1(i)
        if isblack:
            self.bimg.paste( i, (x,y,x+width, y+height),mask=m) 
        else:
            self.rimg.paste( i, (x,y,x+width, y+height),mask=m) 


    def TimeDiffToPixels(self,dt):
       ds = dt.total_seconds() 
       secondsperpixel = (WeatherInfo.FORECAST_PERIOD_HOURS*60*60) / DrawWeather.XSTEP
       return int ( ds / secondsperpixel )



    def Draw(self,ypos,owm):

        xpos=0
        t = datetime.datetime.now()
        dt = datetime.timedelta(hours=WeatherInfo.FORECAST_PERIOD_HOURS)
        tf = t 

        s=sun()  



        for i in range(8):
            
            f = owm.Get(tf)
            if (f==None):
                continue

            #f.Print()

            t_sunrise = s.sunrise(tf)
            t_sunset = s.sunset(tf) 
            
            if (tf<=t_sunrise) and (tf+dt>t_sunrise):
                dx = self.TimeDiffToPixels(t_sunrise-tf)  - self.XSTEP/2
                self.PutImg("sun",0,xpos+dx,ypos-self.YSTEP,False)

            if (tf<=t_sunset) and (tf+dt>t_sunset):
                dx = self.TimeDiffToPixels(t_sunset-tf)  - self.XSTEP/2
                self.PutImg("moon",0,xpos+dx,ypos-self.YSTEP)


            if (i==0):
                self.PutImg("house",0,xpos,ypos+self.YSTEP)
                if (f.t.hour==0): 
                    self.PutImg("ground",1,xpos,ypos+self.YSTEP)
                if (f.t.hour==12): 
                    self.PutImg("ground",2,xpos,ypos+self.YSTEP)
            elif (f.t.hour==0): 
                self.PutImg("ground",1,xpos,ypos+self.YSTEP)
            elif (f.t.hour==12): 
                self.PutImg("ground",2,xpos,ypos+self.YSTEP)
            else:
                self.PutImg("ground",0,xpos,ypos+self.YSTEP)


            wcond = int(f.id/100)

            if (wcond == WeatherInfo.Thunderstorm):
                self.PutImg("thunderstorm",0,xpos,ypos+self.YSTEP)

            if (wcond == WeatherInfo.Atmosphere):
                self.PutImg("fog",0,xpos,ypos+self.YSTEP)


            c = int( (round(float(f.clouds)/10)) )
            self.PutImg("cloud",c,xpos,ypos)

            r = round( f.rain)
            if (r==0) and (f.rain>0.01):
                r=1
            if (r>5):
                r=5
            self.PutImg("rain",r,xpos,ypos+self.YSTEP)

            




            xpos+=self.XSTEP
            tf += dt













class EFrameWeather(EFramePlugin):

    def __init__(self,openwathermap_object):
        self.w = openwathermap_object
        pass



    def Paint(self, xposition, yposition, HEIGHT, WIDTH, options=None):
        df = DrawWeather(self.bimg,self.rimg)
        df.Draw(yposition,self.w)






if __name__ == "__main__":

    import epd7in5b_sock as epd7in5b
    from PIL import Image,ImageDraw,ImageFont
    import PIL.ImageOps 

    HOST = "127.0.0.1"
    epd = epd7in5b.EPD(HOST)


    HBlackimage = Image.new('1', ( epd7in5b.EPD_HEIGHT,epd7in5b.EPD_WIDTH), 255)  
    HRedimage = Image.new('1', (epd7in5b.EPD_HEIGHT,epd7in5b.EPD_WIDTH), 255)  
    df = DrawWeather(HBlackimage,HRedimage)








    print("OpenWeatherMap TEST")
    
    #t = datetime.datetime.now()
    #print(t)

    print("---")

    w = OpenWeatherMap()

    
    w.FromFile("openweathermap.json")

    #w.FromWWW("openweathermap.json")



    w.PrintAll()
    print("---")

    
    #fut = t + datetime.timedelta(hours=2)
    #f = w.Get(fut)
    #f.Print()

    df.Draw(550,w)


    HBlackimage = HBlackimage.transpose(Image.ROTATE_270)
    HRedimage = HRedimage.transpose(Image.ROTATE_270)
        
        
    print("Init...")
    epd.init()
    print("Display...")
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))
    print("Sleep...")
    epd.sleep()




    