import io
import os
import time
from time import sleep
import picamera
import requests
import numpy as np
#from ard import QuadSerial
from base_camera import BaseCamera

numOfCommands = 0
timetotal = 0

class Camera(BaseCamera):
    final_num = None
    theframe = None
    @staticmethod
    def frames(self):
        with picamera.PiCamera() as camera:
            # let camera warm up
            time.sleep(2)
            camera.resolution = (640,480)
            camera.framerate=90
            stream = io.BytesIO()
            global numOfCommands
            global timetotal
            timeFlag = 200
            test = 1;
            thetime = 0;
            oldData = None
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
            #while True:
                # return current frame
                trythis = time.time()
                #camera.capture(stream, 'jpeg')
                stream.seek(0)
                #self.theframe = stream.read()
                self.theframe = stream.getvalue()
                data = np.fromstring(self.theframe, dtype=np.uint8)
                boole = np.array_equal(data, oldData)
                #if the current frame is the same frame as the old frame dont count for fps
                if (boole == True):
                    timeFlag +=1;
                #save the current frame as old frame to check next time if it was changed.
                oldData = data
                #do some manipulating on the data
                data = 1.22*(data)
                #if we took 200 new frames print fps.
                if timeFlag == 0:
                    fps = 200/(thetime)
                    print("manipulated x frames per second: ")
                    print(fps)
                #reduce number of frames to count for fps by 1.
                timeFlag = timeFlag-1
                
                yield self.theframe
                #INSERT IMAGE PROCCESSING ALGORIITHM HERE
                # ------------------ #
                # ------------------ #
                #self.final_num = {"numbers":"world"}
                #data = {"numbers":"world"}
               
                #try:
                #    requests.post("http://192.168.43.180:5000/first_cam", params = data)
                #except:
                #    print("offline.");

                #reset stream for next frame
                stream.seek(0)
                stream.truncate()
                trythis = time.time()-trythis
                thetime+=trythis;
                #print(trythis)
