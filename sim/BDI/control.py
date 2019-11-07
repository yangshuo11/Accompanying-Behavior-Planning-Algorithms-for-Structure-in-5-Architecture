import sys
sys.path.append ('./NAO_SIM')
from ConnectSIM import *
from naoqi import ALProxy

from detector import *
from strategy_c import *
from definition import *
import time
import math

TrainIteration = 1000

if __name__ == '__main__':
	toConnect = connect_sim()


	toConnect.SIM_INIT()
	toConnect.NEW_CONNECT()
	toConnect.initCamera(0)
	toConnect.initCamera(1)
	toConnect.motionInit()
	print("Start Running")
	allSteps = 0
	theCameraID = 1
	checkCount = 0
	signFlag= 1	

	ctrlState = ToControl()
	thePos = []
	theLoc = []

	while(vrep.simxGetConnectionId(toConnect.clientID)!=-1 and allSteps < 1000):
		allSteps += 1
		start = time.time()
		nowImg = toConnect.getImage(theCameraID)
		af = Binarization(nowImg, "red")
		loc_x, loc_y = calcTheLocate(af)
		tPos = toConnect.getObjectPosition()
		obj_pos = tPos[0]
		robotPos = tPos[1]
		theLoc.append([loc_x[0], loc_y[0]])
		thePos.append([robotPos[0], robotPos[1], obj_pos[0], obj_pos[1]])
		print(allSteps)
		print("------------------------------------------------------")
		#print(loc_x, " --- ", loc_y)

		#print(toConnect.motion.getAngles('Body', True))	# The Body Joints data from Sensor
		#print(toConnect.getSensors())
		if loc_x[0] == 0 and loc_y[0] == 0:
			ctrlState.objMissing(toConnect, signFlag)
			theCameraID = 1-theCameraID
			continue
		else:
			ctrlState.checkCount = 0

		endFlag = ctrlState.getCtrlInfo(toConnect, loc_x, loc_y, theCameraID)
		if endFlag:
			break
		if loc_x[0] < 320:
			signFlag = 1
		else:
			signFlag = -1
		# ------ Delay for controling ------ #
		#"""
		timeSteps = 0
		while timeSteps < 20:
			JointControl(toConnect.clientID,toConnect.motion,0,toConnect.Body)
			timeSteps += 1
			time.sleep(0.01)
		#"""
		#print(toConnect.motion.getAngles('Body', False))	# The Body Joints data from Calculated results
		time.sleep(0.01)
		end = time.time()
		#print("Time cost :-> ", end - start)


	doc_loc = open('theLoc.txt', 'w')
	for dA in theLoc:
		for dI in dA:
			doc_loc.write(str(dI))
			doc_loc.write(' ')
		doc_loc.write('\n')

	doc_loc.close()
	
	doc_obj = open('theObj.txt', 'w')
	for dA in thePos:
		for dI in dA:
			doc_obj.write(str(dI))
			doc_obj.write(' ')
		doc_obj.write('\n')
	doc_obj.close()
	