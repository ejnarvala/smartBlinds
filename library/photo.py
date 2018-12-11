import RPi.GPIO as GPIO

class PhotoResistor:
	def __init__(self, pin):
		self.pin_num = pin
		GPIO.setmode(GPIO.BCM)


	def getPhotoVal():
	    RCpin = self.pin_num
	    reading = 0
	    GPIO.setup(RCpin, GPIO.OUT)
	    GPIO.output(RCpin, GPIO.LOW)
	    time.sleep(0.1)

	    GPIO.setup(RCpin, GPIO.IN)
	    # This takes about 1 millisecond per loop cycle
	    while (GPIO.input(RCpin) == GPIO.LOW):
	            reading += 1
	            if(reading > 1500):
	            	return False
	    return reading