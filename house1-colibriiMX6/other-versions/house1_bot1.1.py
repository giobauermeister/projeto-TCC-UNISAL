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

ssl._create_default_https_context = ssl._create_unverified_context #para resolver SSL error

try:
	from urllib.error import URLError
except ImportError:
	from urllib2 import URLError  # python 2

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

	while True:
		monitor()

def monitor():
	global enviado
	global bot
	global frame

	try:
        	update_id = bot.getUpdates()[0].update_id
	except IndexError:
		update_id = None

	for update in bot.getUpdates(offset=update_id, timeout=10):
		chat_id = update.message.chat_id
		#print chat_id
		update_id = update.update_id + 1
		message = update.message.text

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
		#bot.sendMessage(chat_id=chat_id, text="face detected!")
		bot.sendMessage(chat_id=73270008, text="Intrusao detectada em sua residencia!")
		bot.sendMessage(chat_id='@vigiadobairro', text='Atencao! Intrusao detectada em uma residencia do bairro! Visite <a href="http://vigiadobairro.noip.me">Vigia do Bairro</a>.', parse_mode=telegram.ParseMode.HTML)
		saveImage()
		bot.sendPhoto(chat_id=73270008, photo=open('mypic.jpg','rb'))
		#firebase.put('/' , "house1", {u'addr': addrHouse1, u'id': idHouse1, u'visible': "True", u'lat': latHouse1, u'lng': lonHouse1})
		addMarker()
		enviado = True
		print enviado
	if(numberPeople == 0 and enviado is True):
		rmMarker()
		print ("VAZIO")
		#bot.sendMessage(chat_id=chat_id, text="empty")
		enviado = False
		print enviado

def getFrame():
	global camera
	for i in xrange(5):
 		ret, frame = camera.read()
	return frame

def saveImage():
	#frame = getFrame()
	cv2.imwrite('mypic.jpg', frame)

def addMarker():
	firebase.put('/' , "house1", {u'addr': addrHouse1, u'id': idHouse1, u'visible': "True", u'lat': latHouse1, u'lng': lonHouse1})

def rmMarker():
	firebase.put('/' , "house1", {u'addr': addrHouse1, u'id': idHouse1, u'visible': "False", u'lat': latHouse1, u'lng': lonHouse1})

if __name__ == '__main__':
	main()
