#!/usr/bin/env python
#!/usr/bin/env python

import pypot.dynamixel
import time
import itertools
import numpy as np
import xml.etree.ElementTree as ET
import rospy
from std_msgs.msg import String

darwin = {1: 90, 2: -90, 3: 67.5, 4: -67.5, 7: 45, 8: -45, 9: 'i', 10: 'i', 13: 'i', 14: 'i', 17: 'i', 18: 'i'}
abmath = {11: 15, 12: -15, 13: -10, 14: 10, 15: -5, 16: 5}
hand = {5: 60, 6: -60}

path1 = "data.xml"
path2 = "newdata.xml"


class Dynamixel(object) :
	def __init__(self) :
		ports = pypot.dynamixel.get_available_ports()
		if not ports :
			raise IOError("port bhakchodi pel rahe hain")

		print "Is port se judna hai",ports[0]

		self.dxl = pypot.dynamixel.DxlIO(ports[0])
		self.ids = self.dxl.scan(range(25))
		print self.ids
		self.dxl.enable_torque(self.ids)
		if len(self.ids)<20 :
			raise RuntimeError("kuch motor bhakchodi pel rahe hain")
		self.dxl.set_moving_speed(dict(zip(self.ids,itertools.repeat(100))))


	def setSpeed(self,speed,ids) :
		self.dxl.set_moving_speed(dict(zip(ids,itertools.repeat(speed))))

	def setPos(self,pose) :
		pos = {ids:angle for ids,angle in pose.items()}
		self.dxl.set_goal_position(pos)

	def listWrite(self,list) :
		pos = dict(zip(self.ids,list))
		self.dxl.set_goal_position(pos)

	def dictWrite(self,dicti) :
		
		self.dxl.set_goal_position(dicti)

	def angleWrite(self,ids,pose) :
		self.dxl.set_goal_position({ids:pose})
		
	def returnPos(self,ids) :

		return self.dxl.get_present_position((ids,))	



class XML(object) :
	def __init__(self,file) :
		try :
			tree = ET.parse(file)
			self.root = tree.getroot()
		except :
			raise RuntimeError("File nahi mil rahi")

	def parse(self,motion) :
		find = "PageRoot/Page[@name='" +motion+ "']/steps/step"
		steps = [x for x in self.root.findall(find)]
		p_frame = str()
		p_pose = str()
		for step in steps :
			Walk(step.attrib['frame'],step.attrib['pose'],p_frame,p_pose)
			p_frame = step.attrib['frame']
			p_pose = step.attrib['pose']
			
	


class Walk(object) :
	def __init__(self,frame,pose,p_frame,p_pose) :
		self.frame = int(frame)
		self.begin = {}
		self.end = {}
		if not(p_pose) :
			self.frame_diff = 1
			p_pose = pose
		else :
			self.frame_diff = self.frame-int(p_frame) 

		for ids,pos in enumerate(map(float,p_pose.split())) :
			self.end[ids+1]=pos	

		for ids,pos in enumerate(map(float,pose.split())) :
			self.begin[ids+1]=pos
		
		self.set(offsets=[darwin,hand])

	def Offset(self,offset) :
		
		for key in offset.keys() :
			if offset[key] == 'i' :
				self.begin[key] = -self.begin[key]
				self.end[key] = -self.end[key]
			else :
				self.begin[key] += offset[key]
				self.end[key] += offset[key]
		
		

	def set(self,offsets=[]) :
		for offset in offsets :
			self.Offset(offset)
		self.motion() 

	def motion(self) :
		write=[]
		ids=[]
		for key in self.end.keys() :
			linp=np.linspace(self.end[key],self.begin[key],self.frame_diff)
			write.append(linp)
			ids.append(key)	

		for pose in zip(*write) :
			x.setPos(dict(zip(ids,pose)))
			time.sleep(0.0017)

def st_pos():
	w1 = xml1.parse("32 F_S_L")
	#time.sleep(0.01)
	w2 = xml1.parse("33 ")
	#time.sleep(0.01)				

def ft_walk():
	w3 = xml1.parse("38 F_M_R")
	#time.sleep(0.01)	
	w4 = xml1.parse("39 ")
	#time.sleep(0.01)
	w5 = xml1.parse("36 F_M_L")
	#time.sleep(0.01)
	w6 = xml1.parse("37 ")
	#time.sleep(0.01)

def bk_walk():
	w3 = xml2.parse("38 F_M_R")
	#time.sleep(0.01)	
	w4 = xml2.parse("39 ")
	#time.sleep(0.01)
	w5 = xml2.parse("36 F_M_L")
	#time.sleep(0.01)
	w6 = xml2.parse("37 ")
	#time.sleep(0.01)

def listener(data) :
	print data.data

	if data.data >12000 :
		bk_walk()
	else :
		ft_walk()
		
if __name__ == "__name__":
	balance = xml1.parse("152 Balance")
	raw_input("Proceed?")
	rospy.init_node('Dash', anonymous=True)
    	rospy.Subscriber('get_area',String,listener,queue_size=1)
    	rospy.spin()

