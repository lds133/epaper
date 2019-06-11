

import socket
from PIL import Image



PACKET_NONE =     0
PACKET_START =    1
PACKET_CONTINUE = 2
PACKET_STOP =     3
PACKET_CLEAR =    4
PACKET_SLEEP =    5


# Display resolution
EPD_WIDTH       = 640
EPD_HEIGHT      = 384

class EPD:

    DEFAULT_PORT = 5555

    def __init__(self,host,port=0):
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.HOST = host
        if (port!=0):
            self.PORT = port
        else:
            self.PORT = EPD.DEFAULT_PORT
        self.sock=None
        self.pkt=None
        

    # Hardware reset
    def reset(self):
        pass
 
    def packet_start(self):
        self.pkt = bytearray()
        self.pkt.append(0)
        self.pkt.append(0)
        self.pkt.append(0)
        self.pkt.append(0)
        self.pkt.append(0)
        pass

    def packet_append(self,b):
        self.pkt.append(b)
        pass

    def packet_send(self,packettype):
        n = len( self.pkt ) - 4
        self.pkt[0] = n & 0xFF
        self.pkt[1] = (n >> 8) & 0xFF
        self.pkt[2] = (n >> 16) & 0xFF
        self.pkt[3] = (n >> 24) & 0xFF
        self.pkt[4] = packettype

        print("PACKET %i" % n)

        if (self.sock==None):
            self.sock_connect()
            
        print("Sending %i bytes" % len(self.pkt))
        self.sock.sendall(self.pkt)

        self.pkt = None

    def sock_connect(self):
        if (self.sock==None):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Connect to %s:%i" % (self.HOST, self.PORT))
            self.sock.connect((self.HOST, self.PORT))


    def sock_disconnect(self):
        if (self.sock!=None):
            print("Disconnect")
            self.sock.close()
            self.sock = None

    def send_command(self, command):
        pass

    def send_data(self, data):
        pass

    def wait_until_idle(self):
        pass
            
    def init(self):
        self.reset()
        return 0

    def getbuffer(self, image):
        # print "bufsiz = ",(self.width//8) * self.height
        buf = [0xFF] * ((self.width//8) * self.height)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        # print "imwidth = %d, imheight = %d",imwidth,imheight
        if(imwidth == self.width and imheight == self.height):
            print("Horizontal")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[(x + y * self.width) // 8] &= ~(0x80 >> (x % 8))
        elif(imwidth == self.height and imheight == self.width):
            print("Vertical")
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        buf[(newx + newy*self.width) // 8] &= ~(0x80 >> (y % 8))
        return buf

    def display(self, imageblack, imagered):

        self.sock_connect()

        self.packet_start()
        for i in range(0, self.width // 8 * self.height):
            temp1 = imageblack[i]
            temp2 = imagered[i]
            j = 0
            while (j < 8):
                if ((temp2 & 0x80) == 0x00):
                    temp3 = 0x04                #red
                elif ((temp1 & 0x80) == 0x00):
                    temp3 = 0x00                #black
                else:
                    temp3 = 0x03                #white

                temp3 = (temp3 << 4) & 0xFF
                temp1 = (temp1 << 1) & 0xFF
                temp2 = (temp2 << 1) & 0xFF
                j += 1
                if((temp2 & 0x80) == 0x00):
                    temp3 |= 0x04              #red
                elif ((temp1 & 0x80) == 0x00):
                    temp3 |= 0x00              #black
                else:
                    temp3 |= 0x03              #white
                temp1 = (temp1 << 1) & 0xFF
                temp2 = (temp2 << 1) & 0xFF
                self.packet_append(temp3)
                j += 1
        self.packet_send(PACKET_START)

        self.packet_start()
        self.packet_send(PACKET_STOP)

        self.sock_disconnect()
        
        
    def Clear(self, color):

        self.sock_connect()

        self.packet_start()
        self.packet_send(PACKET_CLEAR)

        self.sock_disconnect()
        
        pass


    def sleep(self):

        pass



### END OF FILE ###

