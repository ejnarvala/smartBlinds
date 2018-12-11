from ctypes import *

class IMU:
    def __init__(self):
        path = ".library/lib_imu/liblsm9ds1cwrapper.so"
        self.lib = cdll.LoadLibrary(path)

        self.lib.lsm9ds1_create.argtypes = []
        self.lib.lsm9ds1_create.restype = c_void_p

        self.lib.lsm9ds1_begin.argtypes = [c_void_p]
        self.lib.lsm9ds1_begin.restype = None

        self.lib.lsm9ds1_calibrate.argtypes = [c_void_p]
        self.lib.lsm9ds1_calibrate.restype = None

        self.lib.lsm9ds1_gyroAvailable.argtypes = [c_void_p]
        self.lib.lsm9ds1_gyroAvailable.restype = c_int
        self.lib.lsm9ds1_accelAvailable.argtypes = [c_void_p]
        self.lib.lsm9ds1_accelAvailable.restype = c_int
        self.lib.lsm9ds1_magAvailable.argtypes = [c_void_p]
        self.lib.lsm9ds1_magAvailable.restype = c_int

        self.lib.lsm9ds1_readGyro.argtypes = [c_void_p]
        self.lib.lsm9ds1_readGyro.restype = c_int
        self.lib.lsm9ds1_readAccel.argtypes = [c_void_p]
        self.lib.lsm9ds1_readAccel.restype = c_int
        self.lib.lsm9ds1_readMag.argtypes = [c_void_p]
        self.lib.lsm9ds1_readMag.restype = c_int

        self.lib.lsm9ds1_getGyroX.argtypes = [c_void_p]
        self.lib.lsm9ds1_getGyroX.restype = c_float
        self.lib.lsm9ds1_getGyroY.argtypes = [c_void_p]
        self.lib.lsm9ds1_getGyroY.restype = c_float
        self.lib.lsm9ds1_getGyroZ.argtypes = [c_void_p]
        self.lib.lsm9ds1_getGyroZ.restype = c_float

        self.lib.lsm9ds1_getAccelX.argtypes = [c_void_p]
        self.lib.lsm9ds1_getAccelX.restype = c_float
        self.lib.lsm9ds1_getAccelY.argtypes = [c_void_p]
        self.lib.lsm9ds1_getAccelY.restype = c_float
        self.lib.lsm9ds1_getAccelZ.argtypes = [c_void_p]
        self.lib.lsm9ds1_getAccelZ.restype = c_float

        self.lib.lsm9ds1_getMagX.argtypes = [c_void_p]
        self.lib.lsm9ds1_getMagX.restype = c_float
        self.lib.lsm9ds1_getMagY.argtypes = [c_void_p]
        self.lib.lsm9ds1_getMagY.restype = c_float
        self.lib.lsm9ds1_getMagZ.argtypes = [c_void_p]
        self.lib.lsm9ds1_getMagZ.restype = c_float

        self.lib.lsm9ds1_calcGyro.argtypes = [c_void_p, c_float]
        self.lib.lsm9ds1_calcGyro.restype = c_float
        self.lib.lsm9ds1_calcAccel.argtypes = [c_void_p, c_float]
        self.lib.lsm9ds1_calcAccel.restype = c_float
        self.lib.lsm9ds1_calcMag.argtypes = [c_void_p, c_float]
        self.lib.lsm9ds1_calcMag.restype = c_float

    def startCalibrateIMU(self):
        self.imu = self.lib.lsm9ds1_create()
        self.lib.lsm9ds1_begin(self.imu)
        if self.lib.lsm9ds1_begin(self.imu) == 0:
            print("Failed to communicate with LSM9DS1.")
            quit()
        print("Calibrating IMU, make sure it is horizontal")
        self.lib.lsm9ds1_calibrate(self.imu)
        print("IMU Calibrated.")

    def getAccelVals(self):
        if(self.lib.lsm9ds1_gyroAvailable(self.imu) == 0):
            return False
        else:
            self.lib.lsm9ds1_readAccel(self.imu)
            ax = self.lib.lsm9ds1_getAccelX(self.imu)
            ay = self.lib.lsm9ds1_getAccelY(self.imu)
            az = self.lib.lsm9ds1_getAccelZ(self.imu)

            cax = self.lib.lsm9ds1_calcAccel(self.imu, ax)
            cay = self.lib.lsm9ds1_calcAccel(self.imu, ay)
            caz = self.lib.lsm9ds1_calcAccel(self.imu, az)
            return (cax, cay, caz)