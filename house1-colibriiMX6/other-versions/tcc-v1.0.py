#	Programa TCC V 1.0
#	Detecta face e envia mensagem com numero de pessoas para o telegram
#	Detecta vazio e envia mensagem "empty" para telegram
#	Um sistema de travamento com a flag enviado esta funcionando

import cv2
import telegram 
import ssl

ssl._create_default_https_context = ssl._create_unverified_context #para resolver SSL error

try:
	from urllib.error import URLError
except ImportError:
	from urllib2 import URLError  # python 2

camera_port = 0
camera = cv2.VideoCapture(camera_port)
bodyCascade = cv2.CascadeClassifier('/home/root/haarcascades/haarcascade_frontalface_default.xml')

#main function loop
def main():
	global bot
	bot = telegram.Bot('178110419:AAGC1PAd7tqQyO-ONaw8vApczibRok7ybnM')
	global camera	
	global enviado
	enviado = False

	while True:
		monitor()

def monitor():
	global enviado
	global bot

	try:
        	update_id = bot.getUpdates()[0].update_id
	except IndexError:
		update_id = None

	for update in bot.getUpdates(offset=update_id, timeout=10):
		chat_id = update.message.chat_id
		update_id = update.update_id + 1
		message = update.message.text

	frame = getFrame()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	people = bodyCascade.detectMultiScale(
        	gray,
	        scaleFactor = 1.3,
	        minNeighbors = 3,
        	minSize = (30, 30),
	        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    	)
	for (x, y, w, h) in people:
        	cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
	
	detection = None
	numberPeople = len(people)

	if(numberPeople > 0 and enviado is False):
		print ('Temos ' + str(numberPeople) + ' pessoas.')
		bot.sendMessage(chat_id=chat_id, text="face detected!")
		enviado = True
		print enviado
	if(numberPeople == 0 and enviado is True):
		print ("VAZIO")
		bot.sendMessage(chat_id=chat_id, text="empty")
		enviado = False
		print enviado

def getFrame():
	global camera
	for i in xrange(5):
 		ret, frame = camera.read()
	return frame

def saveImage():
	frame = getFrame()
	cv2.imwrite('mypic.jpg', frame)

if __name__ == '__main__':
	main()
