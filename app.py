from importlib import import_module
import os
#from ard import *
from time import sleep
import time
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
flyFlag=True
flag = False
numOfCommands = 0
timetotal = 0
currentFrame = None
# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)
#ard = QuadSerial()
CORS(app)
theframe = None
def getFrame(camera,*args):
    while 1:
         global theframe
         theframe = camera.theframe
@app.route('/', methods = ["POST"])
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen(camera):
    global flag
    global flyFlag
    global timetotal
    global numOfCommands
    global theframe
    sleep(2)
   
    """Video streaming generator function."""
    try:
        print("new thread try")
        #_thread.start_new_thread(ask_for_numbers,())
        #_thread.start_new_thread(flyDrone,())
        thread.start_new_thread(getFrame,(camera,1))
    except:
        print("can't start new thread")
    #print("hi")
    #_thread.start_new_thread(flyDrone())
    #sleep(2)
    timeFlag=100
    while flag == False:
        #global main_cam_numbers
        #global second_cam_numbers
        #main_cam_numbers=camera.final_num.get('numbers')
        # DO SOMETHING WITH main_cam_numbers AND second_cam_numberes
        # ------------------- #
        # ------------------- #
        # FOR INSTANCE: take 2 strings and print them as below
        #if main_cam_numbers != None and second_cam_numbers != None:
        #    print (main_cam_numbers+" "+second_cam_numbers)
        #if flyFlag == True:
            #ard.send(0.5, 0.5, 0.1, 0.5)
        # END SOMEHTING HERE #
        #theframe = camera.get_frame()    #<-----this function takes too much time. lowering streaming from 50fps to 10-13fps. make it better
        if timeFlag>0:
             numOfCommands = numOfCommands+1
        timeofcommand = time.time()
        theframe = camera.get_frame()
        if theframe!=None:
             yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + theframe + b'\r\n')
        timeofcommand = time.time()-timeofcommand
        if timeFlag>0:
             timetotal+=timeofcommand
        if timeFlag==0:
             print("the fps is:  ")
             print(numOfCommands/timetotal)
             print("average time for a command in seconds: ")
             print(timetotal/numOfCommands)
             print("number of commands/frames sent: ")
             print(numOfCommands)
        timeFlag=timeFlag-1

@app.route('/moveTo', methods=["POST"])
def moveTo():
    ardu = QuadSerial()
    if request.method == 'POST':
        to = request.form['direction']
        print(to)
        if to == 'up':
            ardu.send(0.5, 0.3, 0.02, 0.5)
            #ardu.send(0.5, 0.5, 0.03, 0.5)
        if to == 'down':
            ardu.send(0.5, 0.7, 0.02, 0.5)
            #ardu.send(0.5, 0.5, 0.03, 0.5)
        if to == 'right':
            ardu.send(0.7, 0.5, 0.02, 0.5)
            #ardu.send(0.5, 0.5, 0.03, 0.5)
        if to == 'left':
            ardu.send(0.3, 0.5, 0.02, 0.5)
            #ardu.send(0.5, 0.5, 0.03, 0.5)
    return "moved forward"
def ask_for_numbers():
    """helper function to get numbers from other pi"""
    requests.get("http://zero2.local:5000/get_num", timeout=(20,0.02))
    return 1

def flyDrone():
    #ard = QuadSerial()
    while flyFlag==True:
        ard.send(0.5, 0.5, 0.1, 0.5)
        #ard.send(0.5, 0.5, 0.0, 0.5)
    ard.send(0.5, 0.5, 0.0, 0.5)
@app.route('/startFlying', methods=["POST"])
def start():
    global flyFlag
    flyFlag = True
    return ("starting")

@app.route('/stopFlying', methods=["POST"])
def stop():
    global flyFlag
    flyFlag = False
    ard.send(0.5,0.5,0.0,0.5)
    ard.send(0.5,0.5,0.0,0.5)
    return ("stopping")

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
    app.run(host="0.0.0.0", threaded=True, port=5000)
