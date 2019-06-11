from eframe import MakeEFramePicture

import datetime
import time
b

#HOST = "192.168.0.30"
HOST = "127.0.0.1"

oldd = -1
maxrefreshtime = datetime.timedelta( hours=1 )
lastupdate = datetime.datetime.now()


while(True):


    now = datetime.datetime.now()
    h = now.hour
    m = now.minute
    d = now.day

    if (oldd != d ) or ( (now - lastupdate) > maxrefreshtime):
        oldd = d
        lastupdate = now

        MakeEFramePicture(HOST)


    time.sleep(60)
