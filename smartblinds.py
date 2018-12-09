from flask import Flask, request, render_template, abort, jsonify, make_response
from imu import *
import time
app = Flask(__name__)




@app.route('/', methods=['GET', 'POST'])
def index():
    if(request.method == 'POST'):
        print(request.form)
        tilt = request.form['tilt']
        openTime = request.form['openTime']
        closeTime = request.form['closeTime']
        #TODO: implement/modify something to apply the changes


    return render_template('index.html', data={'light': light, 'tilt': tilt, 'openTime': openTime, 'closeTime': closeTime})



def getPhotoVal():
    #TODO: read the photoresistor and return its value
    return 951


def updateLight():
    global light
    rawPhotoVal = getPhotoVal()
    if(rawPhotoVal):
        light = rawPhotoVal


#spins the motor until blinds are at the provided percent
def setBlindTilt(percent):
    #TODO integrate motor to tilt blinds to this percent
    #spin motor until accelerometer reaches desired val
    return False



#returns the raw accelerometer values
def getAccelVals():
    return (1, 2, 3)
    # if(lib.lsm9ds1_gyroAvailable(imu) == 0):
    #     return False
    # else:
    #     lib.lsm9ds1_readGyro(imu)
    #     ax = lib.lsm9ds1_getAccelX(imu)
    #     ay = lib.lsm9ds1_getAccelY(imu)
    #     az = lib.lsm9ds1_getAccelZ(imu)

    #     cax = lib.lsm9ds1_calcAccel(imu, ax)
    #     cay = lib.lsm9ds1_calcAccel(imu, ay)
    #     caz = lib.lsm9ds1_calcAccel(imu, az)
    #     return (cax, cay, caz)


def updateTilt():
    global tilt
    rawVals = getAccelVals()
    if(rawVals):
        tilt = rawVals[0]



#initializations
if __name__ == '__main__':
    global openTime
    global closeTime
    # lib = startIMU()
    # imu = lib.lsm9ds1_create()
    # lib.lsm9ds1_begin(imu)
    # if lib.lsm9ds1_begin(imu) == 0:
    #     print("Failed to communicate with LSM9DS1.")
    #     quit()
    # lib.lsm9ds1_calibrate(imu)
    # print("IMU Calibrated.")

    #TODO: write a function to open then close the blinds upon startup to
    # set the 0 and 100% values in relation to the accelerometer tilt
    updateLight()
    updateTilt()
    openTime = '06:30'
    closeTime = '21:30'
    app.run(debug=True)