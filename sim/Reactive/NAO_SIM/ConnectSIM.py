import sys
sys.path.append ('./NAO_SIM/VrepAPI')

import vrep
from naoqi import ALProxy
from manage_joints import *
import time

import matplotlib.pyplot as plt
from PIL import Image
import array


class connect_sim(object):
	def __init__(self):
		vrep.simxFinish(-1)
		self.clientID=vrep.simxStart('127.0.0.2',19997,True,True,5000,5)
		print('================ Program Sarted ================')
		if self.clientID!=-1:
			print ('Connected to remote API server')
		else:
			print ('Connection non successful')
			sys.exit('Could not connect')
		print("================ Choregraphes Initialization ================")

		self.naoIP = "127.0.0.1" #raw_input()
		#naoIP = map(str,naoIP.split())
		print ('Enter your NAO port')
		self.naoPort = 10086 #raw_input()
		self.naoPort=int(self.naoPort)
		self.motion = ALProxy("ALMotion",self.naoIP, self.naoPort)
		self.posture = ALProxy("ALRobotPosture", self.naoIP, self.naoPort)
		# Initial data array
		Head_Yaw=[];Head_Pitch=[];
		L_Hip_Yaw_Pitch=[];L_Hip_Roll=[];L_Hip_Pitch=[];L_Knee_Pitch=[];L_Ankle_Pitch=[];L_Ankle_Roll=[];
		R_Hip_Yaw_Pitch=[];R_Hip_Roll=[];R_Hip_Pitch=[];R_Knee_Pitch=[];R_Ankle_Pitch=[];R_Ankle_Roll=[];
		L_Shoulder_Pitch=[];L_Shoulder_Roll=[];L_Elbow_Yaw=[];L_Elbow_Roll=[];L_Wrist_Yaw=[]
		R_Shoulder_Pitch=[];R_Shoulder_Roll=[];R_Elbow_Yaw=[];R_Elbow_Roll=[];R_Wrist_Yaw=[]
		R_H=[];L_H=[];R_Hand=[];L_Hand=[];
		self.Body = [Head_Yaw,Head_Pitch,L_Hip_Yaw_Pitch,L_Hip_Roll,L_Hip_Pitch,L_Knee_Pitch,
			L_Ankle_Pitch,L_Ankle_Roll,R_Hip_Yaw_Pitch,R_Hip_Roll,R_Hip_Pitch,R_Knee_Pitch,
			R_Ankle_Pitch,R_Ankle_Roll,L_Shoulder_Pitch,L_Shoulder_Roll,L_Elbow_Yaw,L_Elbow_Roll,
			L_Wrist_Yaw,R_Shoulder_Pitch,R_Shoulder_Roll,R_Elbow_Yaw,R_Elbow_Roll,R_Wrist_Yaw,L_H,L_Hand,R_H,R_Hand]

		self.camera = []
		self.winPlt = []
		res_rob,self.robotHandle =vrep.simxGetObjectHandle(self.clientID,"NAO",vrep.simx_opmode_oneshot_wait)
		res_obj,self.objHandle =vrep.simxGetObjectHandle(self.clientID,"Cup", vrep.simx_opmode_oneshot_wait)

	
	def SIM_INIT(self):
		#Go to the posture StandInitZero
		initPosture = 'StandZero'
		print ('Posture Initialization : ' + initPosture)
		self.motion.stiffnessInterpolation('Body', 1.0, 1.0)
		self.posture .goToPosture(initPosture, 1.0, 1.0)

		get_first_handles(self.clientID,self.Body)
		print ("================ Handles Initialization ================")
		commandAngles = self.motion.getAngles('Body', False)
		print ('========== NAO is listening ==========')

	def NEW_CONNECT(self):
		print("Init start")
		vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_oneshot)
		time.sleep(2)
		JointInit(self.clientID, 0, self.Body)
		time.sleep(1)
		vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_oneshot)
		time.sleep(3)
		print("Init stop")
	
	def initCamera(self, cameraID):
		if cameraID == 0:
			visionSensorName = 'NAO_vision1'
		else:
			visionSensorName = 'NAO_vision2'
		res1,visionSensorHandle=vrep.simxGetObjectHandle(self.clientID,visionSensorName,vrep.simx_opmode_oneshot_wait)
		res2,resolution,image=vrep.simxGetVisionSensorImage(self.clientID,visionSensorHandle,0,vrep.simx_opmode_streaming)
		time.sleep(0.5)
		#res3,resolution,image=vrep.simxGetVisionSensorImage(self.clientID,visionSensorHandle,0,vrep.simx_opmode_streaming)
		#im = Image.new("RGB", (resolution[0], resolution[1]), "white")

		self.camera.append(visionSensorHandle)

	def getImage(self, cameraID, pause=0.0001):
		res,resolution,image=vrep.simxGetVisionSensorImage(self.clientID,self.camera[cameraID],0,vrep.simx_opmode_buffer)
		#Transform the image so it can be displayed using pyplot
		image_byte_array = array.array('b',image)
		im = Image.frombuffer("RGB", (resolution[0],resolution[1]), image_byte_array, "raw", "RGB", 0, 1)

		im.save("./camImage.png", "PNG")
		time.sleep(pause)

	def stringUnpack():
		return

	def getSensors(self):
		res, theGyro = vrep.simxGetAndClearStringSignal(self.clientID,'TheGyro', vrep.simx_opmode_streaming)
		gData =  theGyro.split()
		gData = list(map(float, gData))
		print("Gyroscope Data -->", theGyro)
		res, theAcce = vrep.simxGetAndClearStringSignal(self.clientID,'TheAcce', vrep.simx_opmode_streaming)
		aData = theAcce.split()
		aData = list(map(float, aData))
		print("Accelerometer Data -->", theAcce)
		return gData, aData

	def getObjectPosition(self):
		res1, objPosition= vrep.simxGetObjectPosition(self.clientID, self.objHandle, -1, vrep.simx_opmode_streaming)
		res2, robPosition= vrep.simxGetObjectPosition(self.clientID, self.robotHandle, -1, vrep.simx_opmode_streaming)
		return objPosition, robPosition

	def motionInit(self):
		print("Init Motion")
		#self.motion.moveInit()
		#JointControl(self.clientID,self.motion,0,self.Body)
		#time.sleep(1)
		self.motion.setWalkTargetVelocity(1.0, 0, 0, 0)
		timeSteps = 0
		while timeSteps < 200:
			JointControl(self.clientID,self.motion,0,self.Body)
			timeSteps += 1
			time.sleep(0.01)

		#self.motion.post.moveTo(0.1, 0, 0)
		#timeSteps = 0
		#while timeSteps < 200:
		#	JointControl(self.clientID,self.motion,0,self.Body)
		#	timeSteps += 1
		#	time.sleep(0.01)
		time.sleep(2)