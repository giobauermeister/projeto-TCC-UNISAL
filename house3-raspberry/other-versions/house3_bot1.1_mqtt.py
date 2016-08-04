# comandos 
# house1
#	python fire-add2.0.py house1 0 True -22.97252054395682 -47.00013929679871
# house2
#	python fire-add2.0.py house2 1 True -22.97300054395682 -47.00020029679871
import requests.packages.urllib3
#requests.packages.urllib3.disable_warnings()

import RPi.GPIO as GPIO

from firebase import firebase
import sys
import telegram

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import ssl

# MQTT Azure IoT Hub Authentication data
auth = {
  'username':"projeto-tcc.azure-devices.net/prj_tcc_house3",
  'password':"SharedAccessSignature sr=projeto-tcc.azure-devices.net%2fdevices%2fprj_tcc_house3&sig=tXsEYKSRHLfNQUrYVCqGYtCq2jjKmvNu3HTH7J%2b8Ej0%3d&se=1473682778"
}
tls = {
  'ca_certs':"/etc/ssl/certs/ca-certificates.crt",
  'tls_version':ssl.PROTOCOL_TLSv1
}


sens1 = 	4;  
switch = 	17;

addrHouse3 = "Escritorio, Valinhos"

idHouse3 = 2

visHouse3 = "False"

latHouse3 = -22.973471
lonHouse3 = -47.00368

firebase = firebase.FirebaseApplication('https://google-maps-api-test.firebaseio.com', None)

def main():
	
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(sens1, GPIO.IN)
	GPIO.setup(switch, GPIO.IN)

	global bot
	bot = telegram.Bot('138543640:AAGdhnII3pcfFf8kSBYCyJPS-WrRr-AwVao') # @house3_bot

	global enviado
	enviado = True

	while True:
		monitor()

def monitor():
		global enviado
		try:
			update_id = bot.getUpdates()[0].update_id
		except IndexError:
			update_id = None

		for update in bot.getUpdates(offset=update_id, timeout=10):
			chat_id = update.message.chat_id
			#print chat_id
			update_id = update.update_id + 1
			message = update.message.text

		if not GPIO.input(switch):			
			rmMarker()
			print "chave ativa, mapa limpo"

		if not GPIO.input(sens1) and enviado is False: # sensor fechado (ativo)
			addMarker()	
			print "sensor ativado"
			sendIotHub()	
			bot.sendMessage(chat_id=73270008, text="Intrusao detectada em sua residencia!")
			bot.sendMessage(chat_id='@vigiadobairro', text="Atencao! Intrusao detectada em uma residencia do bairro! Visite [Vigia do Bairro](http://vigiadobairro.noip.me)", parse_mode=telegram.ParseMode.MARKDOWN)
			enviado = True
		if GPIO.input(sens1) and enviado is True: # sensor aberto (inativo)
			print "sensor desativado"
			enviado = False		

def sendIotHub():
	publish.single("devices/prj_tcc_house3/messages/events/",
  		payload="{'City':'Valinhos','status':1}",
  		hostname="projeto-tcc.azure-devices.net",
  		client_id="prj_tcc_house3",
  		auth=auth,
  		tls=tls,
  		port=8883,
  		protocol=mqtt.MQTTv311)

def addMarker():
	firebase.put('/' , "house3", {u'addr': addrHouse3, u'id': idHouse3, u'visible': "True", u'lat': latHouse3, u'lng': lonHouse3})
def rmMarker():
	firebase.put('/' , "house3", {u'addr': addrHouse3, u'id': idHouse3, u'visible': "False", u'lat': latHouse3, u'lng': lonHouse3})		

if __name__ == "__main__":
	main()


