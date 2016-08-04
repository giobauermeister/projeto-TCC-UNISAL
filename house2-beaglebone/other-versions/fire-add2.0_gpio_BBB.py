# comandos 
# house1
#	python fire-add2.0.py house1 0 True -22.97252054395682 -47.00013929679871
# house2
#	python fire-add2.0.py house2 1 True -22.97300054395682 -47.00020029679871
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

import Adafruit_BBIO.GPIO as GPIO

from firebase import firebase
import sys

sens1 = 	"P9_12";  
sens1off = 	"P8_10";
#sens2 = 	"P8_12";
#sens2off = 	"P8_14";

#addrHouse1 = "Toradex, Valinhos"
addrHouse2 = "Casa, Valinhos"

#idHouse1 = 0
idHouse2 = 1

#visHouse1 = "False"
visHouse2 = "False"
  
#latHouse1 = -22.970471
#lonHouse1 = -47.001353

latHouse2 = -22.971015
lonHouse2 = -47.003675

firebase = firebase.FirebaseApplication('https://google-maps-api-test.firebaseio.com', None)

def main():
	
	GPIO.setup(sens1, GPIO.IN)
	GPIO.setup(sens1off, GPIO.IN)
	#GPIO.setup(sens2, GPIO.IN)
	#GPIO.setup(sens2off, GPIO.IN)

	while True:

		if GPIO.input(sens1):
			#pass
			firebase.put('/' , "house2", {u'addr': addrHouse2, u'id': idHouse2, u'visible': "False", u'lat': latHouse2, u'lng': lonHouse2})
		else:
			#pass
			firebase.put('/' , "house2", {u'addr': addrHouse2, u'id': idHouse2, u'visible': "True", u'lat': latHouse2, u'lng': lonHouse2})
		
		#if GPIO.input(sens2):
			#firebase.put('/' , "house2", {u'addr': addrHouse2, u'id': idHouse2, u'visible': "True", u'lat': latHouse2, u'lng': lonHouse2})
		#else:
			#pass
		
		#if GPIO.input(sens1off):
			#firebase.put('/' , "house1", {u'addr': addrHouse1, u'id': idHouse1, u'visible': "False", u'lat': latHouse1, u'lng': lonHouse1})
		#else:
			#pass

		#if GPIO.input(sens2off):
			#firebase.put('/' , "house2", {u'addr': addrHouse2, u'id': idHouse2, u'visible': "False", u'lat': latHouse2, u'lng': lonHouse2})
		#else:
			#pass

		#result = firebase.put('/' , house, {u'addr': addr, u'id': ID, u'visible': visible, u'lat': lat, u'lng': lng})
		#print result

if __name__ == "__main__":
	main()


