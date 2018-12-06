from flask import Flask
from imu import *
app = Flask(__name__)
@app.route('/')
def index():
    if(lib.lsm9ds1_gyroAvailable(imu) == 0):
        return 'IMU Unavailable'
    else:
        lib.lsm9ds1_readGyro(imu)
        gx = lib.lsm9ds1_getGyroX(imu)
        gy = lib.lsm9ds1_getGyroY(imu)
        gz = lib.lsm9ds1_getGyroZ(imu)

        cgx = lib.lsm9ds1_calcGyro(imu, gx)
        cgy = lib.lsm9ds1_calcGyro(imu, gy)
        cgz = lib.lsm9ds1_calcGyro(imu, gz)
        return 'X: ' + str(cgx) + ',Y: ' + str(cgy) + ',Z: ' + str(cgz)

if __name__ == '__main__':
    lib = startIMU()
    imu = lib.lsm9ds1_create()
    lib.lsm9ds1_begin(imu)
    if lib.lsm9ds1_begin(imu) == 0:
        print("Failed to communicate with LSM9DS1.")
        quit()
    lib.lsm9ds1_calibrate(imu)

    # while True:
    #     while lib.lsm9ds1_gyroAvailable(imu) == 0:
    #         pass
    #     lib.lsm9ds1_readGyro(imu)

    #     gx = lib.lsm9ds1_getGyroX(imu)
    #     gy = lib.lsm9ds1_getGyroY(imu)
    #     gz = lib.lsm9ds1_getGyroZ(imu)

    #     cgx = lib.lsm9ds1_calcGyro(imu, gx)
    #     cgy = lib.lsm9ds1_calcGyro(imu, gy)
    #     cgz = lib.lsm9ds1_calcGyro(imu, gz)


        # print("Gyro: %f, %f, %f [deg/s]" % (cgx, cgy, cgz))
    app.run(debug=True, host='0.0.0.0', port=80)