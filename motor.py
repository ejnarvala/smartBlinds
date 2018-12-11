from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
import time

PWM_DRIVE_A = 21		# ENA - H-Bridge enable pin
FORWARD_A_PIN = 26	# IN1 - Forward Drive
REVERSE_A_PIN = 19	# IN2 - Reverse Drive

motorA = PWMOutputDevice(PWM_DRIVE_A, True, 0, 1000)

forwardA = DigitalOutputDevice(FORWARD_A_PIN)
reverseA = DigitalOutputDevice(REVERSE_A_PIN)

def forward():
    forwardA.value = True
    reverseA.value = False
    motorA = 0.5

def reverse():
    reverseA.value = True
    forwardA.value = False
    motorA = 0.5

if __name__ == "__main__":
    while True:
        forward()
        time.sleep(5)
        reverse()
        time.sleep(5)
