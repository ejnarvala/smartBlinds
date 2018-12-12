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
    global light
    rawPhotoVal = photoRes.getPhotoVal()
    if(rawPhotoVal == False):
        light = 'N/A'
    else:
        light = rawPhotoVal


#spins the motor until blinds are at the provided percent
def setBlindTilt(percentTilt):
    tiltRange = abs(tiltMax - tiltMin)
    tiltTarget = (percentTilt/100.0)*tiltRange + tiltMin
    updateTilt()
    old_tilt = tilt
    if(abs(tilt - tiltTarget) > tiltTolerance):
        return
    busy = True
    if(tiltTarget < tilt):
        motor.startForward()
    else:
        motor.startReverse()
    time.sleep(1.5)
    updateTilt()
    while(abs(tilt - tiltTarget) > tiltTolerance):
        time.sleep(.1)
        updateTilt()
    motor.stop()

    busy = False



def updateTilt():
    global tilt
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
    calibrationTolerance = 4 #tolerence for counting as the same percent
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


    motor = Motor(AIN1_PIN, AIN2_PIN, PWMA_PIN, STBY_PIN, 65)
    print("Calibrating Motor")
    delta = calibrationTolerance + 1
    #tiltBuffer = deque(maxlen=bufferSize)

    #initialize buffer
    #for i in range(bufferSize):
    #    updateTilt()
    #    tiltBuffer.append(tilt)
    #cur_avg = sum(tiltBuffer,0.0) / bufferSize
    updateTilt()
    old_tilt = tilt
    #print("Average Tilt:", cur_avg)
    # start in one direction find max val
    print("Finding min tilt")
    motor.startForward()
    time.sleep(2) #wait 1 second
    updateTilt()
    while(abs(tilt - old_tilt) > calibrationTolerance):
        # print('old tilt:', old_tilt)
        # print('tilt:', tilt)
        old_tilt = tilt
        time.sleep(1)
        updateTilt()
    motor.stop()
    tiltMin = tilt
    print("tilt min:", tiltMin)
    old_tilt = tilt
    #start in opposite direction
    print("Finding max tilt")
    #print(old_tilt, tilt)
    motor.startReverse()
    print('starting reverse')
    time.sleep(5) #wait 1 second
    updateTilt()
    print(old_tilt, tilt)
    while(abs(tilt - old_tilt) > calibrationTolerance):
        # print('old tilt:', old_tilt)
        # print('tilt:', tilt)
        old_tilt = tilt
        time.sleep(1)
        updateTilt()
    motor.stop()
    tiltMax = tilt

    setBlindTilt(50)
    print("tilt max:", tiltMax)
    print("Motor Calibration Finished.")
    time.sleep(10000)

    app.run(debug=True, port=80, host='0.0.0.0')
