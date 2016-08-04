#       Programa TCC V 1.1                                                                        
#       Essa versao detecta face, salva uma foto no sistema e envia para o telegram
#	----------------------------------------------------------------------------
#	Programa TCC V 1.0
#	Detecta face e envia mensagem com numero de pessoas para o telegram
#	Detecta vazio e envia mensagem "empty" para telegram
#	Um sistema de travamento com a flag enviado esta funcionando

import cv2
import telegram 
import ssl
from firebase import firebase

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

import os.path

GPIO_RESET    = False;  # Whether GPIOs should be re-exported
GPIO_PATH     = "/sys/class/gpio";
GPIO_IN  = "in";
GPIO_NUM = "15";

ssl._create_default_https_context = ssl._create_unverified_context #para resolver SSL error

try:
	from urllib.error import URLError
except ImportError:
	from urllib2 import URLError  # python 2

# MQTT Azure IoT Hub Authentication data
auth = {
  'username':"projeto-tcc2.azure-devices.net/prj_tcc_house1",
  'password':"SharedAccessSignature sr=projeto-tcc2.azure-devices.net%2fdevices%2fprj_tcc_house1&sig=VUCewWIq1fZA9cfiIigBxDr82HUzSe6HXZ9pGhRee2Y%3d&se=1466463469"
}
tls = {
  'ca_certs':"/etc/ssl/certs/ca-certificates.crt",
  'tls_version':ssl.PROTOCOL_TLSv1
}

camera_port = 0
camera = cv2.VideoCapture(camera_port)
faceCascade = cv2.CascadeClassifier('/home/root/haarcascades/haarcascade_frontalface_default.xml')
#bodyCascade = cv2.CascadeClassifier('/home/root/haarcascades/haarcascade_fullbody.xml')

addrHouse1 = "Toradex, Valinhos"
idHouse1 = 0
visHouse1 = "False"
latHouse1 = -22.970471
lonHouse1 = -47.001353

firebase = firebase.FirebaseApplication('https://google-maps-api-test.firebaseio.com', None)


#main function loop
def main():
	global bot
	bot = telegram.Bot('236398329:AAHa1h_VOmOdzzcuFKV3Gg6HNUpa96An6WE') # @house1_bot
	global camera	
	global enviado
	enviado = False

	gpioSetup()

	while True:
		monitor()

def monitor():
	global enviado
	global bot
	global frame

	#try:
        	#update_id = bot.getUpdates()[0].update_id
	#except IndexError:
		#update_id = None

	#for update in bot.getUpdates(offset=update_id, timeout=10):
		#chat_id = update.message.chat_id
		#print chat_id
		#update_id = update.update_id + 1
		#message = update.message.text

	frame = getFrame()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	people = faceCascade.detectMultiScale(
        	gray,
	        scaleFactor = 1.3,
	        minNeighbors = 5,
        	minSize = (30, 30),
	        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    	)
	for (x, y, w, h) in people:
        	cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
	
	detection = None
	numberPeople = len(people)

	if(numberPeople > 0 and enviado is False):
		#print ('Temos ' + str(numberPeople) + ' pessoas.')
		print "face detectada"
		#bot.sendMessage(chat_id=chat_id, text="face detected!")
		bot.sendMessage(chat_id=73270008, text="Intrusao detectada em sua residencia!")
		print "Tg chat OK"
		bot.sendMessage(chat_id='@vigiadobairro', text='Atencao! Intrusao detectada em uma residencia do bairro! Visite <a href="http://vigiadobairro.noip.me">Vigia do Bairro</a>.', parse_mode=telegram.ParseMode.HTML)
		print "Tg chan OK"
		saveImage()
		bot.sendPhoto(chat_id=73270008, photo=open('mypic.jpg','rb'))
		print "send photo OK"
		#firebase.put('/' , "house1", {u'addr': addrHouse1, u'id': idHouse1, u'visible': "True", u'lat': latHouse1, u'lng': lonHouse1})
		addMarker()
		sendIotHub()
		enviado = True
		#print "sensor ativado"
		#print enviado
	if(numberPeople == 0 and enviado is True):
		#rmMarker()
		#print ("VAZIO")
		#bot.sendMessage(chat_id=chat_id, text="empty")
		enviado = False
		#print enviado
		print "sensor desativado"

	valueFile = open(GPIO_PATH+'/gpio'+GPIO_NUM+'/value','r')
	output = valueFile.read()
	if "0" in output:
		#print "0"
		rmMarker()
		print "chave ativa, mapa limpo"
	else:
		#print "1"
		pass

def getFrame():
	global camera
	for i in xrange(5):
 		ret, frame = camera.read()
	return frame

def saveImage():
	#frame = getFrame()
	cv2.imwrite('mypic.jpg', frame)

def sendIotHub():
	publish.single("devices/prj_tcc_house1/messages/events/",
  		payload="{'City':'Paulinia','status':1}",
  		hostname="projeto-tcc2.azure-devices.net",
  		client_id="prj_tcc_house1",
  		auth=auth,
  		tls=tls,
  		port=8883,
  		protocol=mqtt.MQTTv311)

def addMarker():
	firebase.put('/' , "house1", {u'addr': addrHouse1, u'id': idHouse1, u'visible': "True", u'lat': latHouse1, u'lng': lonHouse1})

def rmMarker():
	firebase.put('/' , "house1", {u'addr': addrHouse1, u'id': idHouse1, u'visible': "False", u'lat': latHouse1, u'lng': lonHouse1})

def gpioSetup():
	exportFile = open(GPIO_PATH+'/export', 'w')
	unexportFile = open(GPIO_PATH+'/unexport', 'w')

	exportExists = os.path.isdir(GPIO_PATH+'/gpio'+GPIO_NUM)
	if exportExists and GPIO_RESET:
		unexportFile.write(GPIO_NUM)
		unexportFile.flush()

	if not exportExists or GPIO_RESET:
		exportFile.write(GPIO_NUM)
		exportFile.flush()

	directionFile = open(GPIO_PATH+'/gpio'+GPIO_NUM+'/direction','w')
	directionFile.write(GPIO_IN)
	directionFile.flush()	

if __name__ == '__main__':
	main()
