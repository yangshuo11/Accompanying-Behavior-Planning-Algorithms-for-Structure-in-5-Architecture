import sys
import time

from naoConnect import *
from detector import *
from strategy_c import *
from definition import *
from forUtils import *

ITERATION_NUM = 120

if __name__ == '__main__':
	theNao = connect_nao()
	#theNao.getImage(0)
	#theNao.getImage(1)

	theNao.motion.wakeUp()
	theNao.motion.moveInit()
	time.sleep(2)
	theCameraID = 0
	signFlag= 1
	theSelectedColor = "pink"
	ctrlState = ToControl(theNao)

	#nowImg = theNao.getImage(theCameraID)
	#af = Binarization(nowImg, theSelectedColor)
	#setHeadAngle(0, 0.5, theNao.motion)
	#time.sleep(2)
	#"""
	#id = theNao.motion.post.moveTo(0.5, 0, 0)
	#theNao.motion.wait(id, 0)

	#theCameraID = 1
	theObj = []
	theLoc = []
	for iNum in range(ITERATION_NUM):
		print("Step Number -->", iNum)
		nowImg = theNao.getImage(theCameraID)
		af = Binarization(nowImg, theSelectedColor)
		loc_x, loc_y = calcTheLocate(af)
		print loc_x, loc_y
		#print(theNao.motion.getAngles('Body', True))	# The Body Joints data from Sensor
		theLoc.append([loc_x[0], loc_y[0]])
		if loc_x[0] == 0 and loc_y[0] == 0:
			ctrlState.objMissing(theNao, signFlag)
			#theCameraID = 1-theCameraID
			print(" --> 1")
			continue
		else:
			ctrlState.checkCount = 0
			#print(" --> 2")

		endFlag, tDis = ctrlState.getCtrlInfo(theNao, loc_x, loc_y, theCameraID)
		print(tDis)
		theObj.append(tDis)
		if endFlag:
			break
		if loc_x[0] < 320:
			signFlag = 1
		else:
			signFlag = -1

		time.sleep(0.1)

	theNao.motion.post.moveTo(0.1, 0, 0)
	#theNao.motion.moveInit()
	doc_loc = open('theLoc.txt', 'w')
	for dA in theLoc:
		for dI in dA:
			doc_loc.write(str(dI))
			doc_loc.write(' ')
		doc_loc.write('\n')

	doc_loc.close()
	
	doc_obj = open('theObj.txt', 'w')
	for dA in theObj:
		doc_obj.write(str(dA))
		doc_obj.write('\n')
	doc_obj.close()
	
	#"""
