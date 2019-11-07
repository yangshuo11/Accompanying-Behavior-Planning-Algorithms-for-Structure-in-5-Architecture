from naoqi import ALProxy
from PIL import Image
import motion
import cv2
import math
import vision_definitions
import numpy as np
import almath


from forUtils import *

def Binarization(image, pattern="yellow"):
	lower, upper = [], []
	img = cv2.imread("./camImage.png")
	if (pattern == "red"):
		lower = np.array([0, 120, 120])
		upper = np.array([10, 255, 255])
	elif (pattern == "yellow"):
		lower = np.array([20, 100, 100])
		upper = np.array([34, 255, 255])
	elif (pattern == "blue"):
		lower = np.array([110, 70, 70])
		upper = np.array([124, 255, 255])
	# BGR to HSV
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower, upper)
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
	opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
	return opened

def calcTheLocate(img):
	col, row = np.ones(640), np.ones(480)
	colsum, rowsum = [], []
	x, xw, xe = 0,0,0	# w:west -- e:east 
	y, yn, ys = 0,0,0	# n:north -- s:south
	
	for i in range(0, 480):
		product = np.dot(col, img[i][:])
		colsum.append(product)
	for i in range(0, 480):
		if (colsum[i] == max(colsum)):
			y = i
			val = int(max(colsum) / 255)
			yn = i - val
			ys = i + val
			break
	for i in range(0, 640):
		product = np.dot(row, img[:, i])
		rowsum.append(product)
	for i in range(0, 640):
		if (rowsum[i] == max(rowsum)):
			x = i
			val = int(max(rowsum) / 255)
			xw = i - val
			xe = i + val
			break
	loc_x, loc_y = [x, xw, xe], [y, yn, ys]
	return loc_x, loc_y

