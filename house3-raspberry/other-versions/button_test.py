import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

while True:
	if not GPIO.input(17): # sensor ativo
		print GPIO.input(17)
		print "sensor ativo"
	if GPIO.input(17): # sensor inativo	
		print GPIO.input(17)
		print "sensor inativo"
