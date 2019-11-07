import sys
sys.path.append ('./NAO_SIM')

from naoqi import ALProxy
from ConnectSIM import *
from forUtils import *
from definition import *

import time
import math

class ToControl(object):
	"""docstring for toControl"""
	def __init__(self):
		super(ToControl, self).__init__()
		self.checkCount = 0
		self.maxDis = 1.65
		self.aimDis = 0.4

	def objMissing(self, theNao, signFlag):
		if self.checkCount > 2:
			#print("-------- Turn --------")
			theNao.motion.post.moveTo(0, 0, 0.1*signFlag)
			JointControl(theNao.clientID,theNao.motion,0,theNao.Body)
			time.sleep(0.01)
		else:
			self.checkCount += 1

	def getCtrlInfo(self, theNao, loc_x, loc_y, theCameraID):
		endFlag = 0
		if loc_x[2]!= 0 or loc_x[1] != 0:
			nowViewWeight = loc_x[0] -X_LEN/2.0
			t_angle = -VIEW_WEIGHT[0]*nowViewWeight/X_LEN*math.pi / 180

			nowBallPixel = loc_x[2] -loc_x[1]
			nowFigLen = BALL_SIZE*X_LEN/nowBallPixel
			theDis = nowFigLen/(2.0*math.tan(CAMERA_HEIGHT[theCameraID]/2.0))
			if theDis < self.aimDis:
				endFlag = 1
			#print("Dis --> ", theDis)
			theNao.motion.setWalkTargetVelocity(1.0, 0, t_angle/2, 0.2)
			#theNao.motion.post.moveTo(theDis, 0, 0)
		else:
			endFlag = 1

		return endFlag

# TARGET VELOCITY
# motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
