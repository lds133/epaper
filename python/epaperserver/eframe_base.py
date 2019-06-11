#!/usr/bin/python
# -*- coding: utf-8 -*-


class EFramePlugin():

    def SetPaper(self, HBlackImage, HRedImage):
        self.bimg = HBlackImage
        self.rimg = HRedImage


    def Paint(self, xposition, yposition, HEIGHT, WIDTH, options=None):
        pass