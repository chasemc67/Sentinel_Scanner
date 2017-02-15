import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(18, GPIO.OUT)


for i in range(3):
	GPIO.output(18, GPIO.HIGH)
	time.sleep(5)
	GPIO.output(18, GPIO.LOW)
	time.sleep(5)

exit()