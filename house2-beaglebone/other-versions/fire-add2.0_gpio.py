# comandos 
# house1
#	python fire-add2.0.py house1 0 True -22.97252054395682 -47.00013929679871
# house2
#	python fire-add2.0.py house2 1 True -22.97300054395682 -47.00020029679871

import gpio

from firebase import firebase
import sys


SW1 = "15";  
SW2 = "35";
SW3 = "52";

#house = sys.argv[1]
#ID = sys.argv[2]
#visible = sys.argv[3]
#lat = sys.argv[4]
#lng = sys.argv[5]

addrSW1 = "Toradex, Valinhos"
addrSW2 = "Casa, Valinhos"

idSW1 = 0
idSW2 = 1

visSW1 = "False"
visSW2 = "False"
  
latSW1 = -22.970471
lonSW1 = -47.001353

latSW2 = -22.971015
lonSW2 = -47.003675

firebase = firebase.FirebaseApplication('https://google-maps-api-test.firebaseio.com', None)

def main():
	
	gpio.setup(SW1, gpio.IN)
	gpio.setup(SW2, gpio.IN)
	gpio.setup(SW3, gpio.IN)


	while True:
		
		valueSW1 = gpio.read(SW1)
		valueSW2 = gpio.read(SW2)
		valueSW3 = gpio.read(SW3)

		if valueSW1 == 0:
			firebase.put('/' , "house1", {u'addr': addrSW1, u'id': idSW1, u'visible': "True", u'lat': latSW1, u'lng': lonSW1})
		else:
			pass
		
		if valueSW2 == 0:
			firebase.put('/' , "house2", {u'addr': addrSW2, u'id': idSW2, u'visible': "True", u'lat': latSW2, u'lng': lonSW2})
		else:
			pass
		
		if valueSW3 == 0:
			firebase.put('/' , "house1", {u'addr': addrSW1, u'id': idSW1, u'visible': "False", u'lat': latSW1, u'lng': lonSW1})
			firebase.put('/' , "house2", {u'addr': addrSW2, u'id': idSW2, u'visible': "False", u'lat': latSW2, u'lng': lonSW2})
		else:
			pass

		#result = firebase.put('/' , house, {u'addr': addr, u'id': ID, u'visible': visible, u'lat': lat, u'lng': lng})
		#print result

if __name__ == "__main__":
	main()


