
import threading
import time
import os,sys
from PyQt4 import QtGui,QtCore
from PIL import Image,ImageDraw,ImageFont
from PIL.ImageQt import ImageQt

import socket







class MyWidget(QtGui.QWidget  ):


# 00 00 00 00 : size (not included this 4 bytes)
# 00          : id
# 00 00 ...   : data 


    EPD_WIDTH       = 640
    EPD_HEIGHT      = 384

    PACKET_NONE =     0
    PACKET_START =    1
    PACKET_CONTINUE = 2
    PACKET_STOP =     3
    PACKET_CLEAR =    4
    PACKET_SLEEP =    5

    STATE_NONE    =   0
    STATE_HEADER  =   1
    STATE_ID      =   2
    STATE_DATA    =   3

    def __init__(self, parent=None,isvertical=True,isturnover=True):
        QtGui.QWidget.__init__(self)
        
        self.isvertical = isvertical
        self.isturnover = isturnover
        
        self.pic = QtGui.QLabel()
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.pic)
        vbox.addStretch()
        self.setLayout(vbox)
        app.connect(self, QtCore.SIGNAL("ShowImage()"), self.ShowImage)

        palettedata = [ 0, 0, 0,    0, 0, 255,   0, 0, 255,    240, 240, 240,    255, 0, 0,    0, 0, 255,   0, 0, 255,    0, 0, 255]
        self.image = Image.new("P", (self.EPD_WIDTH, self.EPD_HEIGHT),0x03)
        self.image.putpalette(palettedata * 32)
        if (self.isvertical):
            self.image = self.image.transpose(Image.ROTATE_90)
        

        #self.draw = ImageDraw.Draw(self.image)
        #self.draw.rectangle((0, 50, 70, 100), outline = bytes[0])  
        
        self.ResetImage()
        self.ShowImage()


    def ClearImage(self):
        for x in range(self.EPD_WIDTH):
            for y in range(self.EPD_HEIGHT):
                self.image.putpixel((x, y), 3)
        self.x=0
        self.y=0




    def AddDot(self,nibble):
        if (not self.isdrawenabled):
            return
        if (self.isvertical):
            if (self.isturnover):
                self.image.putpixel((self.y  , self.EPD_WIDTH - self.x - 1), nibble)
            else:
                self.image.putpixel((self.EPD_HEIGHT - self.y - 1 , self.x), nibble)
        else:
            self.image.putpixel((self.x, self.y), nibble)
        self.x += 1
        if (self.x >= self.EPD_WIDTH):
            self.x = 0
            self.y += 1
            if (self.y >= self.EPD_HEIGHT):
                self.y = 0
                self.x = 0
                




    def ResetImage(self):
        self.state = self.STATE_HEADER
        self.stateindex = 0
        self.packetsize = 0
        self.packetid = 0
        self.isdrawenabled = False
        print("> RESET ")


    def NewPacket(self):
        if (self.packetid == self.PACKET_START):
            self.y = 0
            self.x = 0
            self.isdrawenabled = True
            print("> PACKET_START %i" % self.packetsize)
            return
        if (self.packetid == self.PACKET_CONTINUE):
            self.isdrawenabled = True
            print("> PACKET_CONTINUE %i" % self.packetsize)
            return
        if (self.packetid == self.PACKET_STOP):
            self.isdrawenabled = True
            print("> PACKET_STOP %i" % self.packetsize)
            return
        if (self.packetid == self.PACKET_CLEAR):
            self.ClearImage()
            print("> PACKET_CLEAR %i" % self.packetsize)
            self.isdrawenabled = False
            return
        if (self.packetid == self.PACKET_SLEEP):
            print("> PACKET_SLEEP %i" % self.packetsize)
            self.isdrawenabled = False
            return

        print("Warning: Wrong packet id %i" % self.packetid)
        self.isdrawenabled = False
        return



    def ProcessByte(self,b):
        if (self.state == self.STATE_HEADER):
            self.packetsize += (int(b) * (0x100 ** self.stateindex))
            print( "%i - %i" % (self.packetsize, self.stateindex))
            self.stateindex += 1
            if (self.stateindex==4):
                self.stateindex = 0
                self.state = self.STATE_ID
            return

        if (self.state == self.STATE_ID):
            self.packetid = b
            self.NewPacket()
            self.state = self.STATE_DATA
            self.stateindex = 1
            print("%i:%i" % (self.packetsize,self.packetid))
            return

        if (self.state == self.STATE_DATA):
            nibble1 = b & 0x0F
            nibble2 = (b >> 4) & 0x0F
            self.AddDot(nibble2)
            self.AddDot(nibble1)
            #print("%i    %i,%i" % (self.stateindex,nibble1,nibble2))
            self.stateindex += 1
            if (self.stateindex>=self.packetsize):
                self.ResetImage()
            return
        if (self.state == self.STATE_NONE):
            self.stateindex += 1
            if (self.stateindex>=self.packetsize):
                self.ResetImage()

                
        print("Error: State mashine broken")
        self.ResetImage()
        return



    def ProcessBytes(self,bytes):
        if (bytes==None):
            self.ResetImage()
            return
        for b in bytes:
            self.ProcessByte(b)
        

    def ShowImageSafe(self):
        self.emit(QtCore.SIGNAL('ShowImage()'))

    def ShowImage(self):
        qim = ImageQt(self.image)
        pix = QtGui.QPixmap.fromImage(qim)
        self.pic.setPixmap(pix)


  
 



window = None





def thread_function(name):


    print("Thread %s: starting" % name)

    HOST = '127.0.0.1' 
    PORT = 5555       

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    print(">>> Socket server on port %i" % PORT)

    while(True):
        print(">>> Waiting...")
        conn, addr = s.accept()
        window.ResetImage()
        print('>>> Connected by %s' % str(addr))
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            n = len(data)
            #print(">>> got %i bytes" % n )

            b = bytearray(n)
            for i in range(n):
                b[i] = ord(data[i])

            window.ProcessBytes(b)
            window.ShowImageSafe()



    print("Thread %s: finishing" % name)















if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    
    x = threading.Thread(target=thread_function, args=(1,))
    x.start()



    sys.exit(app.exec_())

    
    


