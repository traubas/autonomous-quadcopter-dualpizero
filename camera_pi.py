import io
import os
import time
import picamera
import requests
from base_camera import BaseCamera


class Camera(BaseCamera):
    final_num = None
    @staticmethod
    def frames(self):
        with picamera.PiCamera() as camera:
            # let camera warm up
            time.sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True, resize=(400,400)):
                # return current frame
                stream.seek(0)
                frame = stream.read()
                yield frame
                #INSERT IMAGE PROCCESSING ALGORIITHM HERE
                # ------------------ #
                # ------------------ #
                self.final_num = {"numbers":"world"}
                data = {"numbers":"world"}
                #try:
                #    requests.post("http://192.168.43.180:5000/first_cam", params = data)
                #except:
                #    print("offline.");

                #reset stream for next frame
                stream.seek(0)
                stream.truncate()
