from flask import Flask, request, render_template, abort, jsonify, make_response
from imu import *
import time
import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BCM)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
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
    global light
    global tilt
    global openTime
    global closeTime
    updateLight()
    updateTilt()
    data = {
        'light': light,
        'tilt': tilt,
        'openTime': openTime,
        'closeTime': closeTime,
        'busy': True
    }
    return jsonify(data)


def getPhotoVal(RCpin):
    #TODO: read the photoresistor and return its value
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1)
 
    GPIO.setup(RCpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    print('starting reading...')
    while (GPIO.input(RCpin) == GPIO.LOW):
            reading += 1
    return reading
    #return 951


def updateLight():
# TODO: add failcount for disconnects
    global light
    rawPhotoVal = getPhotoVal(LIGHT_PIN)
    #if(rawPhotoVal):
    light = rawPhotoVal


#spins the motor until blinds are at the provided percent
def setBlindTilt(percent):
    #TODO integrate motor to tilt blinds to this percent
    #spin motor until accelerometer reaches desired val
    return False



#returns the raw accelerometer values
def getAccelVals():
    if(lib.lsm9ds1_gyroAvailable(imu) == 0):
        return False
    else:
        lib.lsm9ds1_readAccel(imu)
        ax = lib.lsm9ds1_getAccelX(imu)
        ay = lib.lsm9ds1_getAccelY(imu)
        az = lib.lsm9ds1_getAccelZ(imu)

        cax = lib.lsm9ds1_calcAccel(imu, ax)
        cay = lib.lsm9ds1_calcAccel(imu, ay)
        caz = lib.lsm9ds1_calcAccel(imu, az)
        return (cax, cay, caz)


def updateTilt():
    global tilt
    rawVals = getAccelVals()
    if(rawVals):
        tilt = rawVals[1]



#initializations
if __name__ == '__main__':
    global openTime
    global closeTime
    global light
    global LIGHT_PIN

    #initialize light
    LIGHT_PIN = 18
    GPIO.setmode(GPIO.BOARD)

    #initialize imu
    lib = startIMU()
    imu = lib.lsm9ds1_create()
    lib.lsm9ds1_begin(imu)
    if lib.lsm9ds1_begin(imu) == 0:
        print("Failed to communicate with LSM9DS1.")
        quit()
    print("Calibrating IMU")
    lib.lsm9ds1_calibrate(imu)
    print("IMU Calibrated.")


    print("Checking light sensor")
    light = getPhotoVal(LIGHT_PIN)
    print("Photoresistor value:", light)
    # RCtime(18) provides the reading, higher numbers correspond to darker
    #TODO: write a function to open then close the blinds upon startup to
    # set the 0 and 100% values in relation to the accelerometer tilt
    updateLight()
    updateTilt()
    openTime = '06:30'
    closeTime = '21:30'
    app.run(debug=True, port=80, host='0.0.0.0')
