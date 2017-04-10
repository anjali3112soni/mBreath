# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 21:11:07 2017

@author: Anjali Kumari
"""
import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt


cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
out = cv2.VideoWriter('output.avi',fourcc, 10.0, ( 480,640))


#if vc.isOpened(): # try to get the first frame
#    rval, frame = vc.read()
#else:
#    rval = False
#
#while rval:
#    cv2.imshow("preview", frame)
#    rval, frame = vc.read()
#    print rval
#    key = cv2.waitKey(20)
#    if key == 2: # exit on ESC
#        break
#cv2.destroyWindow("preview")
#vc.release()
firstframe= None
while True:
    grabbed,frame= vc.read()
    text = "unoccupied"
    
    
    
    if not grabbed:
        break
   
    h= int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w=  int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
    
    #frame= imutils.resize(frame,width=600)
   
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    
    
    print 'gray',gray.shape
    print 'frame',frame.shape
    if firstframe is None:
	firstframe = gray
	continue

    frameDelta = cv2.absdiff(firstframe, gray)
    thresh = cv2.threshold(frameDelta,25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    plt.imshow(gray)
    plt.show()
    
    
    (_,cnts,_) = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    
    for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < 10:
			continue
 
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"
    
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    
cv2.destroyWindow("preview")
out.release()
vc.release()
    