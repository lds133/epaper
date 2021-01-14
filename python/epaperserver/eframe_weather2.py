#!/usr/bin/python
# -*- coding: utf-8 -*-

from eframe_base import EFramePlugin
from openweathermap import WeatherInfo,OpenWeatherMap
import datetime
from sunrise import sun

from PIL import Image
import random



class Sprites():

    Black = 0
    White = 1

    BLACK=0
    WHITE=1
    RED  =2
    TRANS=3

    PLASSPRITE = 10
    MINUSSPRITE = 11

    def __init__(self,bimg,rimg):
        self.bimg = bimg
        self.rimg = rimg
        self.bpix = self.bimg.load()
        self.rpix = self.rimg.load()
        self.dir = '../sprite/'
        self.ext = '.png'
        self.w, self.h = bimg.size

    def Draw(self,name,index,xpos,ypos):
    
        #print("DRAW '%s' #%i at %i,%i" % (name,index,xpos,ypos))
    
        imagepath = "%s%s_%02i%s" % (self.dir, name, index, self.ext)
        img = Image.open(imagepath)
        w, h = img.size
        pix = img.load()
        ypos -= h
        for x in range(w):
            for y in range(h):
                if (xpos+x>=self.w) or (xpos+x<0):
                    continue
                if (ypos+y>=self.h) or (ypos+y<0):
                    continue
                if (pix[x,y]==self.BLACK):
                    self.bpix[xpos+x,ypos+y] = self.Black
                    self.rpix[xpos+x,ypos+y] = self.White
                elif (pix[x,y]==self.WHITE):
                    self.bpix[xpos+x,ypos+y] = self.White
                    self.rpix[xpos+x,ypos+y] = self.White
                elif (pix[x,y]==self.RED):
                    self.bpix[xpos+x,ypos+y] = self.White
                    self.rpix[xpos+x,ypos+y] = self.Black

        return w


    DIGITPLAS = 10
    DIGITMINUS = 11
    DIGITSEMICOLON = 12

    def DrawInt(self,n,xpos,ypos,issign=True,isleadzero=False):
        if (n<0):
            sign = self.DIGITMINUS
        else:
            sign = self.DIGITPLAS
        n = round(n)
        n = abs(n)
        n1 = n / 10
        n2 = n % 10
        dx = 0
        if (issign):
            w = self.Draw("digit",sign,xpos+dx,ypos)
            dx+=w+1
        if (n1!=0) or (isleadzero):
            w = self.Draw("digit",n1,xpos+dx,ypos)
            dx+=w+1
        w = self.Draw("digit",n2,xpos+dx,ypos)
        dx+=w+1
        return dx

    def DrawClock(self,xpos,ypos,h,m):
        dx=0
        w = self.DrawInt(h,xpos+dx,ypos,False,True)
        dx+=w
        w = self.Draw("digit",self.DIGITSEMICOLON,xpos+dx,ypos)
        dx+=w
        dx = self.DrawInt(m,xpos+dx,ypos,False,True)
        dx+=w+1
        return dx




    CLOUDWMAX =32
    CLOUDS = [2,3,5,10,30,50]
    CLOUDK = 0.5

    def DrawCloud(self,persent,xpos,ypos,width,height):
        if (persent<2):
            return
        elif (persent<5):
            cloudset = [2]
        elif (persent<10):
            cloudset = [3,2]
        elif (persent<20):
            cloudset = [5,3,2]
        elif (persent<30):
            cloudset = [10,5]
        elif (persent<40):
            cloudset = [10,10]
        elif (persent<50):
            cloudset = [10,10,5]
        elif (persent<60):
            cloudset = [30,5]
        elif (persent<70):
            cloudset = [30,10]
        elif (persent<80):
            cloudset = [30,10,5,5]
        elif (persent<90):
            cloudset = [30,10,10]
        else:
            cloudset = [50,30,10,10,5]

        dx = width 
        dy = 16
        for c in cloudset: 
            self.Draw("cloud",c,xpos+random.randrange(dx),ypos)
        
    HEAVYRAIN = 5.0
    RAINFACTOR = 20

    def DrawRain(self,value,xpos,ypos,width,tline):
        ypos+=1
        r = 1.0 - ( value / self.HEAVYRAIN ) / self.RAINFACTOR 

        for x in range(xpos,xpos+width):
            for y in range(ypos,tline[x],2):
                if (x>=self.w): 
                    continue
                if (y>=self.h): 
                    continue
                if (random.random()>r):
                    self.bpix[x,y] = self.Black
                    self.bpix[x,y-1] = self.Black
        


    def DrawSnow(self,value,xpos,ypos,width,tline):
        pass




    def  DrawWind_degdist(self, deg1,deg2 ):
        h = max(deg1,deg2)
        l = min(deg1,deg2)
        d = h-l
        if (d>180):
            d = 360-d
        return d
    


    def DrawWind_dirsprite(self,dir,dir0,name,list):
        count = [4,3,3,2,2,1,1]
        step = 11.25 #degrees
        dist = self. DrawWind_degdist(dir,dir0)
        n = int(dist/step)
        if (n<len(count)):
            for i in range(0,count[n]):
                list.append(name)
        




    def DrawWind(self,speed,direction,xpos,tline):
            
            list = []

            self.DrawWind_dirsprite(direction,0,  "pine",list)
            self.DrawWind_dirsprite(direction,90, "east",list)
            self.DrawWind_dirsprite(direction,180,"palm",list)
            self.DrawWind_dirsprite(direction,270,"tree",list)

            random.shuffle(list)

            windindex = None
            if   (speed<=0.4):
                windindex = []
            elif (speed<=0.7):
                windindex = [0]
            elif (speed<=1.7):
                windindex = [1,0,0]
            elif (speed<=3.3):
                windindex = [1,1,0,0]
            elif (speed<=5.2):
                windindex = [1,2,0,0]
            elif (speed<=7.4):
                windindex = [1,2,2,0]
            elif (speed<=9.8):
                windindex = [1,2,3,0]
            elif (speed<=12.4):
                windindex = [2,2,3,0]            
            else:
                windindex = [3,3,3,3]    
            
            
            if (windindex!=None):
                ix = int(xpos)
                random.shuffle(windindex)
                j=0
                print("wind>>>",direction,speed,list,windindex);
                for i in windindex:
                    offset = ix+5
                    if (offset>=len(tline)):
                        break
                    self.Draw(list[j],i,ix,tline[offset]+1) 
                    ix+=9
                    j+=1
                





class DrawWeather():










    XSTART = 32
    XSTEP  = 44
    XFLAT =  10

    YSTEP = 50  #64
    
    DEFAULT_DEGREE_PER_PIXEL = 0.5

    @staticmethod
    def mybeizelfnc(t,d0,d1,d2,d3):
        return  (1-t)*( (1-t)*((1-t)*d0+t*d1 ) + t*( (1-t)*d1 + t*d2)) + t*( (1-t)*( (1-t)*d1 + t*d2)+t*((1-t)*d2 +t*d3))


    def mybezier(self,x,xa,ya,xb,yb):
        xc = (xb+xa)/2.0
        d = xb-xa
        t = float(x-xa)/float(d)
        y = DrawWeather.mybeizelfnc(t,ya,ya,yb,yb)
        return int(y)
        #print(t,x,y)




    def __init__(self,bimg,rimg):

        self.bimg = bimg
        self.rimg = rimg
        self.sprite = Sprites(bimg,rimg)
        (self.IMGEWIDTH,self.IMGHEIGHT) = bimg.size


    def TimeDiffToPixels(self,dt):
       ds = dt.total_seconds() 
       secondsperpixel = (WeatherInfo.FORECAST_PERIOD_HOURS*60*60) / DrawWeather.XSTEP
       return int ( ds / secondsperpixel )


    def DegToPix(self,t):
        n = (t - self.tmin)/self.degreeperpixel
        y = self.ypos+self.YSTEP - int(n)
        return y



    #todo: add thunderstorm
    #todo: add fog
    #todo: add snow

    def Draw(self,ypos,owm):



        self.picheight = self.IMGHEIGHT
        self.picwidth = self.IMGEWIDTH
        self.ypos = ypos

        nforecasrt = ( (self.picwidth-self.XSTART)/self.XSTEP ) 
        maxtime = datetime.datetime.now() + datetime.timedelta(hours=WeatherInfo.FORECAST_PERIOD_HOURS*nforecasrt)

        (self.tmin,self.tmax) = owm.GetTempRange(maxtime)
        self.temprange = self.tmax-self.tmin
        if ( self.temprange < self.YSTEP ):
            self.degreeperpixel = self.DEFAULT_DEGREE_PER_PIXEL
        else:
            self.degreeperpixel = self.temprange/float(self.YSTEP)
        
        print("tmin = %f , tmax = %f, range=%f" % (self.tmin,self.tmax,self.temprange))

        xpos=0
        tline = [0]*(self.picwidth+self.XSTEP+1)
        f = owm.GetCurr()
        oldtemp = f.temp
        oldy = self.DegToPix(oldtemp)
        for i in range(self.XSTART):
            tline[i] = oldy
        yclouds = int(ypos-self.YSTEP/2)
        f.Print()

        self.sprite.Draw("house",xpos,0,oldy) 
        self.sprite.DrawInt(oldtemp,xpos+8,oldy+10)
        self.sprite.DrawCloud(f.clouds,xpos,yclouds,self.XSTART,self.YSTEP/2)
        self.sprite.DrawRain(f.rain,xpos,yclouds,self.XSTART,tline)
        self.sprite.DrawSnow(f.snow,xpos,yclouds,self.XSTART,tline)


        t = datetime.datetime.now()
        dt = datetime.timedelta(hours=WeatherInfo.FORECAST_PERIOD_HOURS)
        tf = t 
        
        xpos = int(self.XSTART)
        nforecasrt = int(nforecasrt)

        n = int( (self.XSTEP-self.XFLAT)/2 )
        for i in range(nforecasrt+1):
            f = owm.Get(tf)
            if (f==None):
                continue
            f.Print()
            newtemp = f.temp
            newy = self.DegToPix(newtemp)
            for i in range(n):
                tline[xpos+i] = self.mybezier(xpos+i,xpos,oldy,xpos+n,newy)


            for i in range(self.XFLAT):
                tline[int(xpos+i+n)] = newy
            

            xpos+=n+self.XFLAT

            n = (self.XSTEP-self.XFLAT)
            oldtemp = newtemp
            oldy = newy
            tf += dt

        
        s=sun() 
        tf = t 
        xpos = self.XSTART
        objcounter=0
        for i in range(nforecasrt+1):
            f = owm.Get(tf)
            if (f==None):
                continue

            t_sunrise = s.sunrise(tf)
            t_sunset = s.sunset(tf) 

            ymoon = ypos-self.YSTEP*5/8

            if (tf<=t_sunrise) and (tf+dt>t_sunrise):
                dx = self.TimeDiffToPixels(t_sunrise-tf)  - self.XSTEP/2
                self.sprite.Draw("sun",0,xpos+dx,ymoon)
                objcounter+=1
                if (objcounter==2):
                    break;

            if (tf<=t_sunset) and (tf+dt>t_sunset):
                dx = self.TimeDiffToPixels(t_sunset-tf)  - self.XSTEP/2
                self.sprite.Draw("moon",0,xpos+dx,ymoon)
                objcounter+=1
                if (objcounter==2):
                    break;

            xpos+=self.XSTEP
            tf += dt
        


        istminprinted = False
        istmaxprinted = False
        tf = t 
        xpos = self.XSTART
        n = int( (self.XSTEP-self.XFLAT)/2 )
        for i in range(nforecasrt+1):
            f = owm.Get(tf)
            if (f==None):
                continue

            #f.Print()

            yclouds = int( ypos-self.YSTEP/2 )


            if (f.temp==self.tmin) and (not istminprinted):
                self.sprite.DrawInt(f.temp,xpos+n,tline[xpos+n]+10)
                istminprinted = True

            if (f.temp==self.tmax) and (not istmaxprinted):
                self.sprite.DrawInt(f.temp,xpos+n,tline[xpos+n]+10)
                istmaxprinted = True

            t0 = f.t - dt/2
            t1 = f.t + dt/2



            
            
            # FLOWERS: black - midnight ,  red - midday
            dt_onehour = datetime.timedelta(hours=1);
            dx_onehour = self.XSTEP/WeatherInfo.FORECAST_PERIOD_HOURS
            tt = t0;
            xx = xpos;
            while(tt<=t1):
                ix = int(xx)
                if(tt.hour==12):
                    self.sprite.Draw("flower",1,ix,tline[ix]) 
                if(tt.hour==0):
                    self.sprite.Draw("flower",0,ix,tline[ix]) 
                if(tt.hour==6) or (tt.hour==18) or (tt.hour==3) or (tt.hour==15) or (tt.hour==9) or (tt.hour==21):
                    self.sprite.DrawWind(f.windspeed,f.winddeg,ix,tline)


                tt+=dt_onehour
                xx+=dx_onehour






            self.sprite.DrawCloud(f.clouds,xpos,yclouds,self.XSTEP,self.YSTEP/2)

            self.sprite.DrawRain(f.rain,xpos,yclouds,self.XSTEP,tline)
            self.sprite.DrawSnow(f.snow,xpos,yclouds,self.XSTEP,tline)

            xpos+=self.XSTEP
            tf += dt




        BLACK = 0
        pixel = self.bimg.load()

        for x in range(self.picwidth):
            if (tline[x]<self.picheight):
                pixel[x,tline[x]] = BLACK
            else:
                print("out of range: %i - %i(max %i)" % (x,tline[x],self.picheight))












class EFrameClock(EFramePlugin):

    def __init__(self):
        pass


    def Paint(self, xposition, yposition, HEIGHT, WIDTH, options=None):
        sprite = Sprites(self.bimg,self.rimg)
        now = datetime.datetime.now()
        sprite.DrawClock(xposition, yposition,now.hour,now.minute)
        





class EFrameWeather(EFramePlugin):

    def __init__(self,openwathermap_object):
        self.w = openwathermap_object



    def Paint(self, xposition, yposition, HEIGHT, WIDTH, options=None):
        df = DrawWeather(self.bimg,self.rimg)
        df.Draw(yposition,self.w)


        


if __name__ == "__main__":

    import epd7in5b_sock as epd7in5b
    from PIL import Image,ImageDraw,ImageFont
    import PIL.ImageOps 

    HOST = "127.0.0.1"
    #HOST = "192.168.0.30"
    epd = epd7in5b.EPD(HOST)


    print("Image size %i,%i" % (epd7in5b.EPD_HEIGHT,epd7in5b.EPD_WIDTH))

    HBlackimage = Image.new('1', ( epd7in5b.EPD_HEIGHT,epd7in5b.EPD_WIDTH), 255)  
    HRedimage = Image.new('1', (epd7in5b.EPD_HEIGHT,epd7in5b.EPD_WIDTH), 255)  
    df = DrawWeather(HBlackimage,HRedimage)


    print("OpenWeatherMap TEST")
    
    #t = datetime.datetime.now()
    #print(t)

    print("---")

    w = OpenWeatherMap()

    
    w.FromAuto()



    #w.PrintAll()
    print("---")

    
    #fut = t + datetime.timedelta(hours=2)
    #f = w.Get(fut)
    #f.Print()

    df.Draw(565,w)


    HBlackimage = HBlackimage.transpose(Image.ROTATE_270)
    HRedimage = HRedimage.transpose(Image.ROTATE_270)
        
        
    print("Init...")
    epd.init()
    print("Display...")
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))
    print("Sleep...")
    epd.sleep()




    