import sys
sys.path.append ('./NAO_SIM')

from naoqi import ALProxy
from forUtils import *
from definition import *

import time
import math

class ToControl(object):
	"""docstring for toControl"""
	def __init__(self, theNao):
		super(ToControl, self).__init__()
		StiffnessOn(theNao.motion)
		self.checkCount = 0

	def objMissing(self, theNao, signFlag):
		if self.checkCount > 2:
			#print("-------- Turn --------")
			theNao.motion.post.moveTo(0, 0, 0.2*signFlag)
			time.sleep(0.25)
		else:
			self.checkCount += 1

	def getCtrlInfo(self, theNao, loc_x, loc_y, theCameraID):
		endFlag = 0
		theDis = -1
		if loc_x[2]!= 0 or loc_x[1] != 0:
			print("Turning")
			nowViewWeight = loc_x[0] -X_LEN/2.0
			t_angle = -VIEW_WEIGHT[0]*nowViewWeight/X_LEN*math.pi / 180
			print("Walking")
			nowBallPixel = loc_x[2] -loc_x[1]
			nowFigLen = BALL_SIZE*X_LEN/nowBallPixel
			theDis = nowFigLen/(2.0*math.tan(CAMERA_HEIGHT[theCameraID]/2.0))-0.3
			if theDis < 0.2:
				endFlag = 1
			#print("Dis --> ", theDis)
			theNao.motion.setWalkTargetVelocity(1.0, 0, t_angle/2, 0.5)
			#theNao.motion.setWalkTargetVelocity(1.0, 0, 0, 0.5)
			#theNao.motion.post.moveTo(theDis, 0, 0)
		else:
			endFlag = 1
		"""
		if abs(Y_LEN/2.0-loc_y[0]) > 100:
			#print("Head!!")
			beta = -(((Y_LEN- 2.0*loc_y[0]) / Y_LEN) * 47.64/2) * math.pi / 180
			headAngle = getHeadAngle(theNao.naoIP, theNao.naoPort, theNao.motion)
			beta = beta + headAngle[0]
			#setHeadAngle(0, beta, theNao.motion)
			#theNao.motion.setStiffnesses("Head", 0.0)
			print("Head!! ", headAngle)
		elif(abs(loc_x[0] -X_LEN/2.0) > 150):
			nowViewWeight = loc_x[0] -X_LEN/2.0
			t_angle = -VIEW_WEIGHT[0]*nowViewWeight/X_LEN*math.pi / 180
			print("Turning")
			#theNao.motion.post.moveTo(0, 0, t_angle/2)
			theNao.motion.setWalkTargetVelocity(0, 0, t_angle/2, 0.25)
		elif loc_x[2]!= 0 or loc_x[1] != 0:
			print("Walking")
			nowBallPixel = loc_x[2] -loc_x[1]
			nowFigLen = BALL_SIZE*X_LEN/nowBallPixel
			theDis = nowFigLen/(2.0*math.tan(CAMERA_HEIGHT[theCameraID]/2.0))-0.3
			if theDis < 0.2:
				endFlag = 1
			#print("Dis --> ", theDis)
			theNao.motion.setWalkTargetVelocity(1.0, 0, 0, 0.5)
			#theNao.motion.post.moveTo(theDis, 0, 0)
		else:
			endFlag = 1
		"""
		return endFlag, theDis

# TARGET VELOCITY
# motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
