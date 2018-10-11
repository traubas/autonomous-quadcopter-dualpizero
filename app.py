

from importlib import import_module
import os
import _thread
import requests
from flask import Flask, render_template, Response, request
from flask_cors import CORS
from variables import second_cam_numbers
# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera
main_cam_numbers = None
second_cam_numbers = None

flag = False
# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ["POST"])
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen(camera):
    """Video streaming generator function."""
    try:
        _thread.start_new_thread(ask_for_numbers())
    except:
        print("can't start new thread")
    print("hi")
    while flag == False:
        frame = camera.get_frame()
        global main_cam_numbers
        global second_cam_numbers
        main_cam_numbers=camera.final_num.get('numbers')
        # DO SOMETHING WITH main_cam_numbers AND second_cam_numberes
        # ------------------- #
        # ------------------- #
        # FOR INSTANCE: take 2 strings and print them as below
        if main_cam_numbers != None and second_cam_numbers != None:
            print (main_cam_numbers+" "+second_cam_numbers)
        # END SOMEHTING HERE #
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def ask_for_numbers():
    """helper function to get numbers from other pi"""
    requests.get("http://zero2.local:5000/get_num", timeout=(20,0.02))
    return 1

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_video')
def stop_video():
    flag = True
    return render_template('index.html')

@app.route('/second_cam', methods =["POST"])
def get_numbers_from_second_pi():
    global second_cam_numbers
    if request.method == 'POST':
        num = request.args.get("first")
        print(num)
        #SAVE THE OBJECT FROM SLAVE PI TO THE GLOBAL VARIABLE second_cam_numberes
        second_cam_numbers = num
    return ("thank you")

@app.route('/test_connection', methods = ["POST"])
def test_conn():
    data = "testing connection"
    try:
        requests.post("http://zero2.local:5000/", params = data)
    except:
        return ("error")
    return("exist")

@app.route('/first_cam', methods =["POST"])
def get_numbers():
    global main_cam_numbers
    if request.method == 'POST':
        num = request.args.get("numbers")
        main_cam_numbers = num
        print(main_cam_numbers)
    return ("thanks you")
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
