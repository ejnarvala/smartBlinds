from flask import Flask, request, render_template, abort, jsonify, make_response
from library.imu import IMU
from library.photo import PhotoResistor
from library.motor import Motor
import time
from collections import deque

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/raw/tilt')
def testTilt():
    return str(getAccelVals())

@app.route('/api/raw/light')
def testLight():
    return str(getPhotoVal(18))

@app.route('/api/data')
def api_data():
    updateLight()
    updateTilt()
    data = {
        'light': light,
        'tilt': tilt,
        'openTime': openTime,
        'closeTime': closeTime,
        'busy': busy
    }
    return jsonify(data)


def updateLight():
    rawPhotoVal = photoRes.getPhotoVal()
    if(rawPhotoVal == False):
        light = 'N/A'
    else:
        light = rawPhotoVal


#spins the motor until blinds are at the provided percent
def setBlindTilt(percentTilt):
    delta = tolerance + 1
    updateTilt()
    busy = True
    if(percentTilt < tilt):
        motor.startForward()
    else:
        motor.startReverse()

    avgTilt = tilt
    while(delta > tiltTolerance):
        updateTilt()
        tiltBuffer.append(tilt)
        avgTilt = sum(tiltBuffer, 0.0) / bufferSize
        delta = percentTilt - avgTilt #stop once average Tilt and desired tilt are within tolerecne
    motor.stop()
    busy = False



def updateTilt():
    rawVals = imu.getAccelVals()
    if(rawVals == False):
        tilt = 'N/A'
    else:
        tilt = round(rawVals[1], 2)*100


#initializations
if __name__ == '__main__':
    global openTime
    global closeTime
    global light
    global imu
    global tilt
    global photoRes
    global motor
    global busy
    global tiltMax
    global tiltMin
    global tiltTolerance
    global tiltBuffer
    global bufferSize

    # INIT SETTINGS
    LIGHT_PIN = 18
    AIN1_PIN = 26
    AIN2_PIN = 29
    PWMA_PIN = 12
    STBY_PIN = 13


    # Set Defaults
    openTime = '06:30'
    closeTime = '21:30'
    busy = False
    bufferSize = 5
    calibrationTolerance = 5 #tolerence for counting as the same percent
    tiltTolerance = 5 #percent tolerance for tilting to a percent

    #initialize photoresistor
    photoRes = PhotoResistor(LIGHT_PIN)
    print("Checking light sensor")
    updateLight()
    print("Photoresistor value:", light)


    # initialize IMU
    imu = IMU()
    imu.startCalibrateIMU()
    print("Checking Accelerometer")
    updateTilt()
    print("Accelerometer Y value:", tilt)


    motor = Motor(AIN1_PIN, AIN2_PIN, PWMA_PIN, STBY_PIN)
    print("Calibrating Motor")
    delta = tolerance + 1
    tiltBuffer = deque(maxlen=bufferSize)

    #initialize buffer
    for i in range(bufferSize):
        updateTilt()
        tiltBuffer.append(tilt)
    cur_avg = sum(tiltBuffer,0.0) / bufferSize


    print("Average Tilt:", cur_avg)
    # start in one direction find max val
    print("Finding max tilt")
    motor.startForward()
    while(delta > calibrationTolerance):
        updateTilt()
        tiltBuffer.append(tilt)
        old_avg = cur_avg
        cur_avg = sum(tiltBuffer, 0.0) / bufferSize
        delta = abs(cur_avg - old_avg)
    motor.stop()

    tiltMax = cur_avg
    print("tilt max:", tiltMax)


    #start in opposite direction
    print("Finding min tilt")
    motor.startReverse()
    while(delta > calibrationTolerance):
        updateTilt()
        tiltBuffer.append(tilt)
        old_avg = cur_avg
        cur_avg = sum(tiltBuffer, 0.0) / bufferSize
        delta = abs(cur_avg - old_avg)
    motor.stop()

    tiltMin = cur_avg
    print("tilt min:", tiltMin)
    print("Motor Calibration Finished.")

    app.run(debug=True, port=80, host='0.0.0.0')