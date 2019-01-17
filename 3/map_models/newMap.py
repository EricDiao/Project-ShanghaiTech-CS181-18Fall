import random, traceback, sys, os
sys.path.append("..")
import itertools
from math import sin,cos,sqrt,pi,acos
from util import Counter



class Map:
	def __init__(self):
		self._horizontalActions = ["L_30","L_60","R_60","R_30","S"]
		self._verticalActions = ["up","down","None"]
		self._speedActions = [8,-8,0]
		self._heightResolution = 300
		self._lengthResolution = 2500
		self._widthResolution = 2500
		runwayLocation1 = (30.560549,103.951040)
		runwayLocation2 = (30.516492,103.936683)
		self._airportElevation = 496
		self._left = 102.28
		self._right = 106.22
		self._lower = 29.51 
		self._upper = 31.13
		self._radius = 6371000
		self._maxX,self._maxY = self.XYInDistToCoordinate(self.longLaToXYInDist((self._upper,self._right)))
		self._maxZ = (6000 - 1000) // self._heightResolution
		# print('maxXYZ:',self._maxX,self._maxY,self._maxZ)
		self.runwayLocationCoordinate1 = self.XYInDistToCoordinate(self.longLaToXYInDist(runwayLocation1))
		self.runwayLocationCoordinate2 = self.XYInDistToCoordinate(self.longLaToXYInDist(runwayLocation2))
		self._map = []
		for a in range(self._maxX + 1):
			self._map.append([])
			for b in range(self._maxY + 1):
				self._map[a].append([])
				for c in range(self._maxZ + 1):
					if c != 0:
						if a == 0 or a == self._maxX or b == 0 or b == self._maxY:
							self._map[a][b].append(-50)
						else:
							self._map[a][b].append(3 * (self._maxZ - c))
					elif c == 0:
						if ((a,b) != self.runwayLocationCoordinate1) and ((a,b) != self.runwayLocationCoordinate2):
							self._map[a][b].append(-100)
						else:
							self._map[a][b].append(100)
		self._actions = []
		for horizontalAction in self._horizontalActions:
			for verticalAction in self._verticalActions:
				for speedAction in self._speedActions:
					self._actions.append((horizontalAction,verticalAction,speedAction))
		# print("mapsize:",len(self._map),len(self._map[0]),len(self._map[0][0]))
		# print(self.runwayLocationCoordinate1,self.runwayLocationCoordinate2)
		# print(self._map[45][74][0],self._map[45][74][1],self._map[45][74][2],self._map[45][74][3])
		self.values = Counter()
		self.tempValue = Counter()

	def longLaToXYInDist(self,position):
		# distX = self._radius * cos(location[0]) * (location[1] - self._left) * pi / 180
		# distY = self._radius * cos(location[1] - self._left)
		C = sin(self._left)*sin(self._left)*cos(position[0]-self._lower)+cos(self._left)*cos(self._left)
		distX = self._radius*pi/180*acos(C)
		C = sin(self._left)*sin(position[1])+cos(self._left)*cos(position[1])
		distY = self._radius*pi/180*acos(C)
		return distX,distY

	def XYInDistToLongLa(self,location):
		latitude = self._lower + location[1] / 111000
		longtitude = self._left + location[0] * 180 / (self._radius * cos(latitude) * pi)
		return latitude,longtitude

	def XYInDistToCoordinate(self,location):
		return int(location[0] // self._lengthResolution), int(location[1] // self._widthResolution)

	def getPossibleActions(self,state):
		tempActions = self._actions[:]
		for action in self._actions:
			# print('iniaction:',action)
			nextState = self.getNextState(state,action)
			X,Y = self.XYInDistToCoordinate((nextState[0][0],nextState[0][1]))
			# print('getPossibleActions:',nextState[0])
			if (X < 0) or (X > self._maxX) or\
				(Y < 0) or (Y > self._maxY) or\
				(nextState[0][2] < 1000) or (nextState[0][2] > 6000) or\
				(nextState[1][1] < 100 or nextState[1][1] > 250):
				# print('getPossibleActions altitude:',tempActions)
				# print('currentaction:',action)
				tempActions.remove(action)
		return tempActions

	def getNextState(self,state,action):
		hAction = action[0]
		vAction = action[1]
		sAction = action[2]
		# print(hAction,vAction,sAction)
		height = state[0][2]
		speed = state[1][1]
		heading = state[1][0]
		if heading < 15 or heading > 345:
			heading = 0
		if hAction == "L_30":
			heading -= 30
			if heading < 0:
				heading += 360
		elif hAction == "L_60":
			heading -= 60
			if heading < 0:
				heading += 360
		elif hAction == "R_30":
			heading += 30
			if heading > 360:
				heading -= 360
		elif hAction == "R_60":
			heading += 60
			if heading > 360:
				heading -= 360
		if vAction == "up":
			height += 300
		elif vAction == "down":
			height -= 300
		averageSpeed = (2 * speed + sAction) / 2
		speed += sAction
		xSpeed = speed * sin(heading)
		ySpeed = speed * cos(heading)
		distX,distY = state[0][0],state[0][1]
		distX += xSpeed * 20
		distY += ySpeed * 20
		return (distX,distY,height),(heading,speed)
