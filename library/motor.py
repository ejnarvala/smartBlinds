import RPi.GPIO as GPIO
import time

class Motor:
	def __init__(self, AIN1, AIN2, PWMA, STBY, SPEED=1):
		self.AIN1_PIN = AIN1
		self.AIN2_PIN = AIN2
		self.PWMA_PIN = PWMA
		self.STBY_PIN = STBY
		self.speed = SPEED
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.AIN1_PIN, GPIO.OUT)
		GPIO.setup(self.AIN2_PIN, GPIO.OUT)
		GPIO.setup(self.PWMA_PIN, GPIO.OUT)
		GPIO.setup(self.STBY_PIN, GPIO.OUT)

	def setSpeed(speed):
		self.speed = speed

	def startForward(self):
		GPIO.output(self.AIN1_PIN, GPIO.HIGH) # Set AIN1
		GPIO.output(self.AIN2_PIN, GPIO.LOW) # Set AIN2

		#TODO: change this to PWM for variable speed
		GPIO.output(self.PWMA_PIN, GPIO.HIGH)

		GPIO.output(self.STBY, GPIO.HIGH)

	def startReverse(self):
		GPIO.output(self.AIN2_PIN, GPIO.HIGH) # Set AIN1
		GPIO.output(self.AIN1_PIN, GPIO.LOW) # Set AIN2

		#TODO: change this to PWM for variable speed
		GPIO.output(self.PWMA_PIN, GPIO.HIGH)
		
		GPIO.output(self.STBY, GPIO.HIGH)

	def stop(self):
		GPIO.output(self.STBY_PIN, GPIO.LOW) # Set STBY
		GPIO.output(self.AIN1_PIN, GPIO.LOW) # Set AIN1
		GPIO.output(self.AIN2_PIN, GPIO.LOW) # Set AIN2

		#change to PWM
		GPIO.output(self.PWMA_PIN, GPIO.LOW) # Set PWMA
