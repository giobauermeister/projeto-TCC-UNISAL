# comandos 
# house1
#	python fire-add2.0.py house1 0 True -22.97252054395682 -47.00013929679871
# house2
#	python fire-add2.0.py house2 1 True -22.97300054395682 -47.00020029679871

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import time

import Adafruit_BBIO.GPIO as GPIO

from firebase import firebase
import sys
import telegram

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import ssl

# MQTT Azure IoT Hub Authentication data
auth = {
  'username':"projeto-tcc2.azure-devices.net/prj_tcc_house2",
  'password':"SharedAccessSignature sr=projeto-tcc2.azure-devices.net%2fdevices%2fprj_tcc_house2&sig=nBxpllWJKC9xwc3KmQ6ETRUUEPIXQ9GlhwsWUwyBy%2fg%3d&se=1466463488"
}
tls = {
  'ca_certs':"/etc/ssl/certs/ca-certificates.crt",
  'tls_version':ssl.PROTOCOL_TLSv1
}

sens1 = 	"P9_12";  
switch = 	"P8_10";

addrHouse2 = "Casa, Valinhos"

idHouse2 = 1

visHouse2 = "False"

latHouse2 = -22.971015
lonHouse2 = -47.003675

firebase = firebase.FirebaseApplication('https://google-maps-api-test.firebaseio.com', None)

def main():
	
	GPIO.setup(sens1, GPIO.IN)
	GPIO.setup(switch, GPIO.IN)

	global bot
	bot = telegram.Bot('199894232:AAFEVmPbSYdB8IwYg-o8wg62YrwEPoXzhuU') # @house2_bot

	global enviado
	enviado = True

	while True:
		monitor()

def monitor():
		global enviado
		#try:
			#update_id = bot.getUpdates()[0].update_id
		#except IndexError:
			#update_id = None

		#for update in bot.getUpdates(offset=update_id, timeout=10):
			#chat_id = update.message.chat_id
			#print chat_id
			#update_id = update.update_id + 1
			#message = update.message.text

		if GPIO.input(switch) == 1:
			rmMarker()
			print "chave ativa, mapa limpo"	

		if not GPIO.input(sens1) and enviado is False: # sensor fechado (ativo)
			addMarker()	
			print "sensor ativado"
			sendIotHub()
			#print "IoT Hub OK"	
			bot.sendMessage(chat_id=73270008, text="Intrusao detectada em sua residencia!")
			print "Tg chat OK"
			time.sleep(1)
			bot.sendMessage(chat_id='@vigiadobairro', text="Atencao! Intrusao detectada em uma residencia do bairro! Visite [Vigia do Bairro](http://vigiadobairro.noip.me)", parse_mode=telegram.ParseMode.MARKDOWN)
			print "Tg chan OK"
			enviado = True
		if GPIO.input(sens1) and enviado is True: # sensor aberto (inativo)
			print "sensor desativado"
			enviado = False		

def sendIotHub():
	publish.single("devices/prj_tcc_house2/messages/events/",
  		payload="{'City':'Campinas','status':1}",
  		hostname="projeto-tcc2.azure-devices.net",
  		client_id="prj_tcc_house2",
  		auth=auth,
  		tls=tls,
  		port=8883,
  		protocol=mqtt.MQTTv311)

def addMarker():
	firebase.put('/' , "house2", {u'addr': addrHouse2, u'id': idHouse2, u'visible': "True", u'lat': latHouse2, u'lng': lonHouse2})
def rmMarker():
	firebase.put('/' , "house2", {u'addr': addrHouse2, u'id': idHouse2, u'visible': "False", u'lat': latHouse2, u'lng': lonHouse2})		

if __name__ == "__main__":
	main()


