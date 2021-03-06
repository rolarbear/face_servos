import cv
import time
import Image
import serial
import math

#cv.NamedWindow("camera", 1)
capture = cv.CreateCameraCapture(0)

#s = serial.Serial(port='/dev/ttyUSB0', baudrate = 9600)	#screen
s = serial.Serial(port='/dev/ttyUSB0', baudrate = 115200) 	#arduino

xPos = 0x5A
yPos = 0x73
xServo = 0x41
yServo = 0x42


time.sleep(2);		#wait for arduino to  reset

s.write(chr(0x00))

s.write(chr(xServo))	#X servo flag
s.write(chr(xPos))	#x servo position
s.write(chr(yServo))	#Y servo flag
s.write(chr(yPos))	#y servo position

width = None
height = None
width = 320
height = 240

if width is None:
    width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
else:
	cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)    

if height is None:
	height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
else:
	cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height) 

result = cv.CreateImage((width,height),cv.IPL_DEPTH_8U,3) 

def Load():

	return (faceCascade, eyeCascade)

def Display(image):
	cv.NamedWindow("Red Eye Test")
	cv.ShowImage("Red Eye Test", image)
	cv.WaitKey(0)
	cv.DestroyWindow("Red Eye Test")

def DetectRedEyes(image, faceCascade, eyeCascade):
	min_size = (20,20)
	image_scale = 2
	haar_scale = 1.2
	min_neighbors = 2
	haar_flags = 0

	# Allocate the temporary images
	gray = cv.CreateImage((image.width, image.height), 8, 1)
	smallImage = cv.CreateImage((cv.Round(image.width / image_scale),cv.Round (image.height / image_scale)), 8 ,1)

	# Convert color input image to grayscale
	cv.CvtColor(image, gray, cv.CV_BGR2GRAY)

	# Scale input image for faster processing
	cv.Resize(gray, smallImage, cv.CV_INTER_LINEAR)

	# Equalize the histogram
	cv.EqualizeHist(smallImage, smallImage)

	# Detect the faces
	faces = cv.HaarDetectObjects(smallImage, faceCascade, cv.CreateMemStorage(0),
	haar_scale, min_neighbors, haar_flags, min_size)

	# If faces are found
	if faces:
		global  xPos, yPos
		for ((x, y, w, h), n) in faces:
		# the input to cv.HaarDetectObjects was resized, so scale the
		# bounding box of each face and convert it to two CvPoints
			#pt1 = (int(x * image_scale), int(y * image_scale))
			#pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
			#cv.Rectangle(image, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
			face_region = cv.GetSubRect(image,(x,int(y + (h/4)),w,int(h/2)))
			#face_center = (int(x + (w/2))), (int(y + (h/2)))
			#print face_center
			posBuff = 7
			camSteps = 1
			if xPos > 0x00 & xPos < 0xB4:
				if (int(x + (w/2)) > (width/4)) & (math.fabs(int(x + (w/2)) - (width/4)) > posBuff):

					new_xPos = (xPos + camSteps)
					s.write(chr(xServo))
					s.write(chr(new_xPos))
					#print "X"
					#print new_xPos
					xPos = new_xPos
				if (int(x + (w/2)) < (width/4)) & (math.fabs(int(x + (w/2)) - (width/4)) > posBuff):
					new_xPos = (xPos - camSteps)
					s.write(chr(xServo))
					s.write(chr(new_xPos))
					#print "X"
					#print new_xPos
					xPos = new_xPos
			if yPos > 0x32 & yPos < 0xB4:
				if (int(y + (h/2)) > (height/4)) & (math.fabs(int(y + (h/2)) - (height/4)) > posBuff):
					new_yPos = (yPos + camSteps)
					s.write(chr(yServo))
					s.write(chr(new_yPos))
					#print "Y"
					#print new_yPos
					yPos = new_yPos
				if (int(y + (h/2)) < (height/4)) & (math.fabs(int(y + (h/2)) - (height/4)) > posBuff):
					new_yPos = (yPos - camSteps)
					s.write(chr(yServo))
					s.write(chr(new_yPos))
					#print "Y"
					#print new_yPos
					yPos = new_yPos
			#s.write(chr(yServo))	#Y servo flag
			#height 

			#s.write(chr(0xFE))
			#s.write(chr(0x01))
			#s.write(str(face_center))
			

		#cv.SetImageROI(image, (pt1[0],
			#pt1[1],
			#pt2[0] - pt1[0],
			#int((pt2[1] - pt1[1]) * 0.7)))
		eyes = cv.HaarDetectObjects(image, eyeCascade,
		cv.CreateMemStorage(0),
		haar_scale, min_neighbors,
		haar_flags, (15,15))	

		#if eyes:
			# For each eye found
			#for eye in eyes:
				# Draw a rectangle around the eye
				#cv.Rectangle(image,
				#(eye[0][0],
				#eye[0][1]),
				#(eye[0][0] + eye[0][2],
				#eye[0][1] + eye[0][3]),
				#cv.RGB(255, 0, 0), 1, 8, 0)

	cv.ResetImageROI(image)
	return image

faceCascade = cv.Load("/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml")
eyeCascade = cv.Load("/usr/local/share/OpenCV/haarcascades/haarcascade_eye.xml")

while True:
	img = cv.QueryFrame(capture)

	image = DetectRedEyes(img, faceCascade, eyeCascade)
#	cv.ShowImage("camera", image)				#
#	k = cv.WaitKey(10);					#
#	if k == 'f':						#
#		break						#
