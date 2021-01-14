#!/usr/bin/python
# -*- coding: utf-8 -*-

from eframe_base import EFramePlugin
import time
import datetime
from PIL import Image,ImageDraw,ImageFont








class EFrameCalendar(EFramePlugin):

    def __init__(self):

        fontfile = '../pic/arial.ttf'
        bdfontfile = '../pic/arialbd.ttf'
        lnfontfile = '../pic/ARIALN.TTF'


        self.font_btiny = ImageFont.truetype(bdfontfile, 14)
        self.font_tiny = ImageFont.truetype(fontfile, 14)
        self.font_big = ImageFont.truetype(bdfontfile, 200)
        self.font_small = ImageFont.truetype(fontfile, 30)
        self.font_med = ImageFont.truetype(lnfontfile, 120)


        #self.monnames = [u"Січня",u"Лютого",u"Березня",u"Квітня",u"Травня",u"Червня",u"Липня",u"Серпня",u"Вересня",u"Жовтня",u"Листопада",u"Грудня"]
        #self.downames = [u"Понеділок",u"Вівторок",u"Середа",u"Четвер ",u"П'ятниця",u"Субота",u"Неділя"]
        self.monnames = [u"Січень",u"Лютий",u"Березень",u"Квітень",u"Травень",u"Червень",u"Липень",u"Серпень", u"Вересень",u"Жовтень",u"Листопад",u"Грудень"]
        self.downames = [u"ПН",u"ВТ",u"СР",u"ЧТ ",u"ПТ",u"СБ",u"НД"]




    def GetDaysCount(self,year0,mon0):
        year1 = year0
        mon1 = mon0+1
        if (mon1==13):
            mon1=1
            year1+=1
        return ( datetime.date(year1, mon1, 1) -  datetime.date(year0, mon0, 1)).days
    

    


    def Paint(self, xposition, yposition, HEIGHT, WIDTH, options=None):
        
        now = datetime.datetime.now()

        h = now.hour
        m = now.minute
        d = now.day

        

        dow = now.weekday()
        mon = now.month
        year = now.year
        monstr = self.monnames[mon-1]    
        dowstr = self.downames[dow]

        drawblack = ImageDraw.Draw(self.bimg)
        drawred = ImageDraw.Draw(self.rimg)
        dowstr_w, dowstr_h = drawblack.textsize(dowstr,font = self.font_med)

        if (dow>4):
            drawdow = drawred
        else:
            drawdow = drawblack

    
        # TEXT

        ypos = 0

        day_y_shift = -35
        daystr = str(d)
        #daystr_w, daystr_h = drawblack.textsize(daystr,font = self.font_big)
        daystr_x = ypos
        drawdow.text((daystr_x, ypos+day_y_shift), str(daystr), font = self.font_big, fill = 0)

        dow_x_shift = 0
        dow_y_shift = -15
        dowstr_w, dowstr_h = drawblack.textsize(dowstr,font = self.font_med)
        dowstr_x = (HEIGHT -dowstr_w)
        drawdow.text((dowstr_x+dow_x_shift, ypos+dow_y_shift ), dowstr, font = self.font_med, fill = 0)


        ypos+=120
        monstr_w, monstr_h = drawblack.textsize(monstr,font = self.font_small)
        monstr_x = dowstr_x + (dowstr_w - monstr_w)/2
        drawblack.text((monstr_x, ypos), monstr, font = self.font_small, fill = 0)




        # PROGRESS BAR
        ypos = ypos+55
        xpos = 0
        mondays = self.GetDaysCount(year,mon)
        
        xstep = HEIGHT / mondays
        ystep = xstep
        d = 1
        day = now.day
        while (d <= mondays):
            t = datetime.datetime(year, mon, d,1,0,0)
            if (t.weekday()>4):
                drawdow = drawred
            else:
                drawdow = drawblack

            if (d==day):
                drawdow.chord((xpos-2, ypos-2, xpos+xstep-2, ypos+ystep-2), 0, 360 ,fill=0  )
                drawdow.chord((xpos+2, ypos+2, xpos+xstep-6, ypos+ystep-6), 0, 360 ,fill=1  )
            else:
                if (d<=day):
                    drawdow.chord((xpos, ypos, xpos+xstep-4, ypos+ystep-4), 0, 360 ,fill=0  )
                else:
                    drawdow.arc((xpos, ypos, xpos+xstep-4, ypos+ystep-4), 0, 360 ,fill=0  )
            xpos+=xstep
            d+=1
        




        ycal   = ypos+20


        t = datetime.datetime(year, mon, 1,1,0,0)
        t_weekday = t.weekday()
        ts = t - datetime.timedelta(days =  t.weekday())

        
        xpos0 = -3
        ypos = ycal
        xpos = xpos0 
        ystep = 17
        xstep = 27

        fontxmove=5
        fontymove=5
        tga = 0.577
        circyshift = 2
        circxshift = 2
        lineyshift = -2


        weekflag = False
        while ((ts.month+ts.year*12)<=(t.month+t.year*12)):

            #print(ts,xpos,ypos)

           

            if (ts>=t):
                if (ts.weekday()>4):
                    drawdow = drawred
                else:
                    drawdow = drawblack

                if (ts<now):
                    textfont = self.font_btiny
                else:
                    textfont = self.font_tiny

                

                s = str(ts.day)
                s_w, s_h = drawblack.textsize(s,font = textfont)

                drawdow.text((xpos + ( xstep - s_w) , ypos), s , font = textfont, fill = 0)

                if (ts.day==now.day):
                    drawblack.arc((xpos+( xstep - s_w)-fontxmove-circxshift, ypos-circyshift , xpos+xstep+fontxmove+circxshift, ypos+ystep), 0, 360, fill = 0)


            if (ts.weekday()==6):
                if (weekflag):
                    ypos+=ystep
                    xpos = xpos0
                    weekflag = False
                else:
                    xpos += xstep
                    weekflag = True
            else:
                xpos += xstep



            ts += datetime.timedelta(days =  1)



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
    
    cal = EFrameCalendar()
    cal.SetPaper( HBlackImage, HRedImage)

    cal.Paint( 0,0,epd7in5b.EPD_HEIGHT, epd7in5b.EPD_WIDTH, None)



    HBlackImage = HBlackImage.transpose(Image.ROTATE_270)
    HRedImage = HRedImage.transpose(Image.ROTATE_270)
        
        
    print("Init...")
    epd.init()
    print("Display...")
    epd.display(epd.getbuffer(HBlackImage), epd.getbuffer(HRedImage))
    print("Sleep...")
    epd.sleep()
