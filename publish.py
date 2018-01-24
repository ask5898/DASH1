#!/usr/bin/env python


import cv2
import numpy as np
import time
import rospy
from std_msgs.msg import String
y,u,v = 0,101,80


def getArea() :
	cap = cv2.VideoCapture(1)
	'''width,height = cap.get(3),cap.get(4)
	cap.set(3,width/5)
	cap.set(4,height/5)'''
	
	flag1=False
	t=time.time()
	rec=True
	while rec:
		rec,img = cap.read()
		img_yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
	
		blur = cv2.GaussianBlur(img_yuv,(11,11),2)
		ball = cv2.inRange(blur, (np.array([0,u-30,v-30])), (np.array([255,u+30,v+30])))
		im_floodfill = ball.copy()
		h, w = ball.shape[:2]
		mask = np.zeros((h+2, w+2), np.uint8)
		cv2.floodFill(im_floodfill, mask, (0,0), 255)
		fill = cv2.bitwise_and(im_floodfill,im_floodfill,mask = ball)
	
		
	
		#images,s_contour,hierarchy = cv2.findContours(crop_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	
		images,contour,hierarchy = cv2.findContours(fill,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		
		cv2.drawContours(img, contour, -1, (0,255,0), 2)




		if len(contour)>0:
			cnt = contour[0]
			area = cv2.contourArea(cnt)
			print area
			return area

		else:
			pass
		cv2.imshow(" ",img)
		if cv2.waitKey(1)&0xff==27:
		    break



def talker() :
   
        #msg=raw_input()
        pub=rospy.Publisher('get_area',String,queue_size=10)
        rospy.init_node('talker',anonymous=True) 
        rate=rospy.Rate(10)

        while not rospy.is_shutdown() :
	    msg = getArea() 
            pub.publish(msg)
        


if __name__=="__main__" :
    try :
        talker()

    except rospy.ROSInterruptException :
        pass



