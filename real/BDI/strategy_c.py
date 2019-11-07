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
		self.MAX_DIS = 1.8
		self.SAVE_DIS = 0.25
		self.old_X_pos = 0
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
		a_rate = 0.5
		theDis = -1

		now_X_pos = X_LEN/2.0-loc_x[0]
		if abs(self.old_X_pos-now_X_pos) > 100:
			a_rate = a_rate*1.25
		else:
			a_rate = a_rate*0.75
		self.old_X_pos = now_X_pos

		if loc_x[2]!= 0 or loc_x[1] != 0:
			print("Turning")
			nowViewWeight = loc_x[0] -X_LEN/2.0
			t_angle = -VIEW_WEIGHT[0]*nowViewWeight/X_LEN*math.pi / 180
			print("Walking")
			nowBallPixel = loc_x[2] -loc_x[1]
			nowFigLen = BALL_SIZE*X_LEN/nowBallPixel
			theDis = nowFigLen/(2.0*math.tan(CAMERA_HEIGHT[theCameraID]/2.0))-0.3
			if theDis < self.SAVE_DIS:
				endFlag = 1

			tDis = theDis
			if tDis > self.MAX_DIS:
				tDis = self.MAX_DIS
			dRate = 0.5*(tDis - self.SAVE_DIS)/(self.MAX_DIS-self.SAVE_DIS)+0.5
			#print("Dis --> ", theDis)
			theNao.motion.setWalkTargetVelocity(1.0, 0, a_rate*t_angle, 0.18*dRate)
			#theNao.motion.setWalkTargetVelocity(1.0, 0, t_angle/2, 0.5)
		else:
			endFlag = 1
		
		return endFlag, theDis

# TARGET VELOCITY
# motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
