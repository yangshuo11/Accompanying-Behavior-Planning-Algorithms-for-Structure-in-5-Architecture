from naoqi import ALProxy
from PIL import Image
import motion
import cv2
import math
import vision_definitions
import numpy as np
import almath

def getHeadAngle(IP, PORT, motionProxy):
	# motionProxy = ALProxy("ALMotion",IP,PORT)
	actuator = ["HeadYaw", "HeadPitch"]
	useSensor = False
	headAngle = motionProxy.getAngles(actuator, useSensor)

	return headAngle

def getHeadPitchAngle(IP, PORT, motionProxy):
	# motionProxy = ALProxy("ALMotion",IP,PORT)
	actuator = "HeadPitch"
	useSensor = False
	headAngle = motionProxy.getAngles(actuator, useSensor)
	
	return headAngle

def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def setHeadAngle(alpha, beta, motionProxy):
	# motionProxy = ALProxy("ALMotion", IP, PORT)
	motionProxy.setStiffnesses("Head", 1.0)
	maxSpeedFraction = 0.3
	names = ["HeadYaw", "HeadPitch"]
	angles = [alpha, beta]
	#print(angles)
	# beta : [-0.5, 0.5]
	motionProxy.angleInterpolationWithSpeed(names, angles, maxSpeedFraction)
	motionProxy.setStiffnesses("Head", 0.0)