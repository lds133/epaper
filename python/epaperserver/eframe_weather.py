#!/usr/bin/python
# -*- coding: utf-8 -*-

from eframe_base import EFramePlugin
from openweathermap import Forecast,OpenWeatherMap,DrawWeather

class EFrameWeather(EFramePlugin):

    def __init__(self):
        pass




    def Paint(self, xposition, yposition, HEIGHT, WIDTH, options=None):
        w = OpenWeatherMap()
        #w.FromFile("openweathermap.json")
        #w.FromWWW("openweathermap.json")
        w.FromAuto("openweathermap.json")
        df = DrawWeather(self.bimg,self.rimg)
        df.Draw(yposition,w)