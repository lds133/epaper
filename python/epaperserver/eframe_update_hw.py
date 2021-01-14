from eframe import MakeEFramePicture
from multiprocessing import Process
import time


def MakePicture():
    HOST = "192.168.1.55"
    MakeEFramePicture(HOST)

    
    
    
if __name__ == '__main__':

    maxrunntime_sec = 300

    print("Execution time limit "+str(maxrunntime_sec)+" sec.")

    p = Process(target=MakePicture)
    p.start()
    p.join( maxrunntime_sec )

    if p.is_alive():
        print("It's killing time...")
        p.terminate()
        p.join()






