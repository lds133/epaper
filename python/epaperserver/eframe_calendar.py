#!/usr/bin/python
# -*- coding: utf-8 -*-

from eframe_base import EFramePlugin
import time
import datetime
from PIL import Image,ImageDraw,ImageFont


class EFrameCalendar(EFramePlugin):

    def __init__(self):

        fontfile = '../pic/miamanueva.ttf'

        self.font_tiny = ImageFont.truetype(fontfile, 27)
        self.font_big = ImageFont.truetype(fontfile, 85)
        self.font_small = ImageFont.truetype(fontfile, 40)
        self.font_med = ImageFont.truetype(fontfile, 50)


        self.monnames = [u"Січня",u"Лютого",u"Березня",u"Квітня",u"Травня",u"Червня",u"Липня",u"Серпня",u"Вересня",u"Жовтня",u"Листопада",u"Грудня"]
        self.downames = [u"Понеділок",u"Вівторок",u"Середа",u"Четвер ",u"П'ятниця",u"Субота",u"Неділя"]




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
    

        line1_shift = 5
        line2_shift = 100
        line3_shift = 120
        cal_shift = 80


        yline1 = line1_shift
        yline2 = yline1+line2_shift
        yline3 = yline2+line3_shift
        ycal   = yline3+cal_shift

        drawblack = ImageDraw.Draw(self.bimg)
        drawred = ImageDraw.Draw(self.rimg)
        dowstr_w, dowstr_h = drawblack.textsize(dowstr,font = self.font_med)
                     
        dowstr_x = (HEIGHT -dowstr_w)/2
        if (dow>4):
            drawred.text((dowstr_x, yline1), dowstr, font = self.font_med, fill = 0)
        else:
            drawblack.text((dowstr_x, yline1), dowstr, font = self.font_med, fill = 0)
            
        daystr = str(d)
        daystr_w, daystr_h = drawblack.textsize(daystr,font = self.font_big)
        daystr_x = (HEIGHT -daystr_w)/2
        drawblack.text((daystr_x, yline2), str(daystr), font = self.font_big, fill = 0)

        monstr_w, monstr_h = drawblack.textsize(monstr,font = self.font_small)
        monstr_x = (HEIGHT -monstr_w)/2
        drawblack.text((monstr_x, yline3), monstr, font = self.font_small, fill = 0)

        #drawred.text((500, 100), clockstr, font = self.font_tiny, fill = 0)


        t = datetime.datetime(year, mon, 1,1,0,0)
        ts = t - datetime.timedelta(days =  t.weekday())




        
        xpos0 = -3
        ypos = ycal
        xpos = xpos0 
        ystep = 45
        xstep = 54

        fontxmove=5
        fontymove=5
        tga = 0.577
        circyshift = 3
        circxshift = 2

        

        while(ts.month<=t.month):
            #print(ts,xpos,ypos)


            s = str(ts.day)
            s_w, s_h = drawblack.textsize(s,font = self.font_tiny)
            if (ts>=t):
                if (ts.weekday()>=5):
                    drawred.text((xpos + ( xstep - s_w) , ypos), s , font = self.font_tiny, fill = 0)
                else:
                    drawblack.text((xpos + ( xstep - s_w) , ypos), s , font = self.font_tiny, fill = 0)

                #drawred.rectangle((xpos+( xstep - s_w), ypos , xpos+xstep, ypos+ystep),  outline = 0)

                if (ts.day==now.day):
                    drawblack.arc((xpos+( xstep - s_w)-fontxmove-circxshift, ypos-circyshift , xpos+xstep+fontxmove+circxshift, ypos+ystep), 0, 360, fill = 0)
                elif (ts<now):
                    dy = s_w*tga
                    lx1 = xpos+( xstep - s_w)
                    ly1 = ypos + (ystep-dy)/2 
                    lx2 = xpos+xstep
                    ly2 = ly1+ dy
                    drawred.line((lx1,ly1, lx2, ly2),fill = 1)
                    drawred.line((lx1,ly1+1, lx2, ly2+1),fill = 1)
                    drawblack.line((lx1,ly1, lx2, ly2),fill = 0)
                    drawblack.line((lx1,ly1+1, lx2, ly2+1),fill = 0)

                    #drawblack.line((xpos+xstep, ypos , xpos+( xstep - s_w), ypos+ystep),  fill = 0)



            if (ts.weekday()==6):
                ypos+=ystep
                xpos = xpos0
            else:
                xpos += xstep

            ts += datetime.timedelta(days =  1)
