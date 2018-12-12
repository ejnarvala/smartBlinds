from flask import Flask, request, render_template, abort, jsonify, make_response
from library.imu import IMU
from library.photo import PhotoResistor
from library.motor import Motor
import time
import datetime
from collections import deque
import threading

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/raw/tilt')
def testTilt():
    return str(getAccelVals())

@app.route('/api/target', methods=['POST'])
def updateTimes():
    global openTime
    global closeTime
    payload = request.json
    openTime = payload['openTimeTarget']
    closeTime = payload['closeTimeTarget']
    print('Open time updated to:', openTime)
    print('Close time updated to:', closeTime)

@app.route('/api/raw/light')
def testLight():
    return str(getPhotoVal(18))

@app.route('/api/openBlind')
def api_openBlind():
    try:
        openBlind()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/closeBlind')
def api_closeBlind():
    try:
        closeBlind()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/data')
def api_data():

    updateLight()
    updateTilt()
    data = {
        'light': light,
        'tilt': tilt,
        'openTime': openTime,
        'closeTime': closeTime,
        'busy': busy,
        'isOpen': isOpen
    #    'isClosed': isClosed
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
    if(tiltTarget > tilt):
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



def openBlind():
    global tilt
    global isOpen
#    global isClosed
    if (tilt > zeroTilt):
        print("starting forward")
        motor.startForward()
       # while abs(tilt - zeroTilt) > calibrationTolerance:
        while tilt > zeroTilt:
            print("Tilt " + str(tilt))
            updateTilt()
    elif (tilt < zeroTilt):
        print("starting reverse")
        motor.startReverse()
#        while abs(tilt - zeroTilt) > calibrationTolerance:
        while tilt < zeroTilt:
            print("Tilt " + str(tilt))
            updateTilt()
    motor.stop()
   # isClosed = False
    isOpen = True


def closeBlind():
    global tilt
    global isOpen
    if (tilt < tiltMin):
        print("starting reverse")
        motor.startReverse()
       # while abs(tilt - tiltMin) > calibrationTolerance:
        while tilt < tiltMin:
            print("Tilt " + str(tilt))
            updateTilt()

    elif (tilt > tiltMin):
        print("starting forward")
        motor.startForward()
        while tilt > tiltMin:
#        while abs(tilt - tiltMin) > calibrationTolerance:
            print("Tilt " + str(tilt))
            updateTilt()
    motor.stop()
    isOpen = False
  #  isClosed = True


def checkTime():
    global openTime
    global closeTime
    global hasBeenClocked


    while(True):
        now = datetime.datetime.now()
        currHour = int(now.hour)
        currMinute = int(now.minute)

        a = openTime.split(":")
        b = closeTime.split(":")
        openHour = int(a[0])
        openMinute = int(a[1])
        closeHour = int(b[0])
        closeMinute = int(b[1])

        if not hasBeenClocked and openHour == currHour and openMinute == currMinute:
            hasBeenClocked = not hasBeenClocked
            openBlind()
        elif hasBeenClocked and closeHour == currHour and closeMinute == currMinute:
            hasBeenClocked = not hasBeenClocked
            closeBlind()

        time.sleep(30)



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
    global zeroTilt
    global isOpen
   # global isClosed
    global hasBeenClocked

    # INIT SETTINGS
    LIGHT_PIN = 18
    AIN1_PIN = 26
    AIN2_PIN = 19
    PWMA_PIN = 12
    STBY_PIN = 13


    # Set Defaults
    openTime = '06:30'
    closeTime = '21:30'
    hasBeenClocked = False
    busy = False
    bufferSize = 5
    calibrationTolerance = 5 #tolerence for counting as the same percent
    tiltTolerance = 5 #percent tolerance for tilting to a percent
    isOpen = False
   # isClosed = True

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


    motor = Motor(AIN1_PIN, AIN2_PIN, PWMA_PIN, STBY_PIN, 55)
    print("Calibrating Motor")
    #delta = calibrationTolerance + 1
    #tiltBuffer = deque(maxlen=bufferSize)

    #initialize buffer
    #for i in range(bufferSize):
    #    updateTilt()
    #    tiltBuffer.append(tilt)
    #cur_avg = sum(tiltBuffer,0.0) / bufferSize
    updateTilt()
    old_tilt = tilt
    zeroTilt = tilt
    #print("Average Tilt:", cur_avg)
    # start in one direction find max val
    print("Finding min tilt")
    now = time.time()
    motor.startForward()
    time.sleep(1.5)
    updateTilt()
    while(abs(tilt - old_tilt) > calibrationTolerance or (time.time() - now) > 10):
        # print('old tilt:', old_tilt)
        print('tilt:', tilt)
        old_tilt = tilt
        time.sleep(1)
        updateTilt()
    motor.stop()
    tiltMin = tilt
    print("tilt min:", tiltMin)
    print("Motor Calibration Finished.")
    print("Zero Tilt" + str(zeroTilt))
    
    threading.Thread(target=checkTime.start()

    app.run(port=80, host='0.0.0.0')
