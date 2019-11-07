import sys
import time

# Python Image Library
import Image

from naoqi import ALProxy
# To get the constants relative to the video.
import vision_definitions

class connect_nao(object):
	def __init__(self):
		#self.naoIP = "192.168.8.168"
		self.naoIP = "192.168.8.179"
		self.naoPort = 9559

		self.resolution = 2    # VGA
		self.colorSpace = 11   # RGB
		#self.camProxy = []
		#self.videoClient = []
		self.camProxy = ALProxy("ALVideoDevice", self.naoIP, self.naoPort)
		"""
		for i in range(2):
			tCamProxy = ALProxy("ALVideoDevice", self.naoIP, self.naoPort)
			tCamProxy.setParam(vision_definitions.kCameraSelectID, i)
			tVideoClient = tCamProxy.subscribe("python_client", resolution, colorSpace, 5)
			self.camProxy.append(tCamProxy)
			self.videoClient.append(tVideoClient)
		"""

		self.motion = ALProxy("ALMotion", self.naoIP, self.naoPort)
		self.posture = ALProxy("ALRobotPosture", self.naoIP, self.naoPort)
		self.posture.goToPosture("StandInit", 0.5)
		time.sleep(2)
		self.memoryProxy = ALProxy("ALMemory", self.naoIP, self.naoPort)

		
	def getImage(self, cameraID,pause=0.0001):
		self.camProxy.setParam(vision_definitions.kCameraSelectID, cameraID)
		videoClient = self.camProxy.subscribe("python_client", self.resolution, self.colorSpace, 5)
		naoImage = self.camProxy.getImageRemote(videoClient)
		self.camProxy.unsubscribe(videoClient)
		#naoImage = self.camProxy[cameraID].getImageRemote(self.videoClient[cameraID])
		#self.camProxy[cameraID].unsubscribe(self.videoClient[cameraID])
		"""
		imageWidth = naoImage[0]
		imageHeight = naoImage[1]
		array = naoImage[6]
		"""
		im = Image.frombytes("RGB", (naoImage[0], naoImage[1]), naoImage[6])
		im.save("camImage.png", "PNG")
		time.sleep(pause)
		#im.show()
		#return 0

	def getSensors(self):
		GyrX = memoryProxy.getData("Device/SubDeviceList/InertialSensor/GyrX/Sensor/Value")
		GyrY = memoryProxy.getData("Device/SubDeviceList/InertialSensor/GyrY/Sensor/Value")
		GyrZ = memoryProxy.getData("Device/SubDeviceList/InertialSensor/GyrZ/Sensor/Value")
		#print ("Gyrometers value X: %.3f, Y: %.3f" % (GyrX, GyrY))
		gyrData = [GyrX, GyrY, GyrZ]
		# Get the Accelerometers Values
		AccX = memoryProxy.getData("Device/SubDeviceList/InertialSensor/AccX/Sensor/Value")
		AccY = memoryProxy.getData("Device/SubDeviceList/InertialSensor/AccY/Sensor/Value")
		AccZ = memoryProxy.getData("Device/SubDeviceList/InertialSensor/AccZ/Sensor/Value")
		accData = [AccX, AccY, AccZ]
		#print ("Accelerometers value X: %.3f, Y: %.3f, Z: %.3f" % (AccX, AccY,AccZ))
		return gyrData, accData


