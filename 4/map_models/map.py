# This part is the construction of a discrete description of a map.
# First, construct a map with landscape.
# Then, get data from each airplane about its location and other data, reflect them on the map.
# Finally build several function in rewarding and penalty associating with planes' relative locations.
# As I have not got the data of the map, I will not give proper data to the map, instead I will seperate data input and map building. 
# So the map will not be biult in this commit, but the method and the requirements of data will be provided.
# Note: It's a statistic map model, not containing time iteration.
import sys
sys.path.append("..")
from airplane_models.airplane import baseAirplane
from math import sin,cos,sqrt

class controlTower():
	"""
	get data from approach control and pass it back to appoach control if any plane is not able to land or has taken off.

	this class is not finished
	"""
	def __init__(self, numRunway=None, landingInterval=None, takeoffInterval=None):
		pass

	def checkRunwayAvailability(self,runwayNumber):
		#check whether a runway is available
		pass

	def checkLandingRequest(self,inputFlight):
		#Check correlated runway if a plane can land at this time
		pass

	def returnToApproachControl(self,Flight):
		#Give command to a plane to wait for landing by reentering approach control area.
		pass

	def checkTakeoffRequest(self,inputFlight):
		#check all runways if a flight is able to take off
		pass

	def handOver(self,flight):
		#return an airplane structure with the runway number, In order to pass to approach control
		pass

class approachControlArea():
	"""
	Map constructor for approaching control and position examiner for AIAC project.

	this class is not finished
	"""

	def __init__(self, leftMost=None, rightMost=None, upperMost=None, lowerMost=None, \
			lengthResolution=None, widthResolution=None, numRunway=2, \
			runwayLocations=[[(30.563688,103.940061),(30.593320,103.953838)],[(30.519631,103.936683),(30.549429,103.950609)]],\
			airportElevation=None, windDirections=None, mapData=None,):
		self._numRunway = numRunway
		self._numSpecArea = numRunway * 2
		self._airportElevation = airportElevation
		# Take airport's elevation as groud elevation.
		self._map = []
		# Inintialize a 3D array to specify the map (somehow like Minecraft) discretely, of where there is land and to make position judgment easier.
		self._windDirections = windDirections
		# Wind flow is crucial in determining the direction of landing & takeoff, generally, takeoff and landing both go agaist the wind. For CTU, usually the  is 
		self._leftMost = leftMost
		self._rightMost = rightMost
		self._upperMost = upperMost
		self._lowerMost = lowerMost
		# All ___Mosts are in rad of longtitude and latitude, lengths will be computed with average radius of earth;
		self._maxHeight = 6000
		# Generally only airplanes under 6000 meters height would be taken over by approaching control,
		self._minHeight = 1000
		# And airplane under 1000 meters would be taken over by control tower.
		"***NOT DETERMINED!!!!***"
		self._heightResolution = 1000
		self._widthResolution = widthResolution
		self._lengthResolution = lengthResolution
		# PENALTY: If a plane enter an occupied pixel, take it as crashed.
		# Note: these 3 value have not been determined yet.
		self._length = int(abs(cos(abs(self._upperMost) * 6371000 * abs(self._leftMost - self._rightMost))) // self._lengthResolution + 1)
		self._width = int(abs(self._upperMost - self._lowerMost) * 6371000) // self._widthResolution + 1
		self._height = int(self._maxHeight - self._minHeight) // self._heightResolution + 1
		# Pixel numbers of each direction
		self._crashCounter = 0
		self._mislandingCounter = 0
		# Penalty counters
		self._runwayLocations = runwayLocations
		"""
			This is the location of the head of the runway (a list contains tuples indicating loctions of the two end of a runway),
			Sample: 
											[[(2.11,0.62),(2.13,0.54)],[...]]
											   -----   -----   --------
												|        |        |
										  Southern    Northern    other runways(if any)
			From the runway we get a threshold region of where the planes should leave the approach control region.
			Note: usually the control tower would 
			PENALTY: When an airplane goes below 1000 meters outside a threshold region or heading to the wrong direction when leaving the threshold region, we take it as mislanding.
		"""
		self._runwayDirections = {}
		# directions of runways
		counter = 0
		if runwayLocations != None:
			for runway in self._runwayLocations:
				# diffLeftToRight = (runway[0][0] - runway[1][0]) * cos(runway[0][1])
				# diffUpToDown = (runway[0][1] - runway[1][1])
				# self._runwayDirections[counter] = (diffUpToDown,diffLeftToRight)
				self._runwayDirections[counter] = (1,0)
				counter += 1
		# Computing runway directions
		self._mapData = mapData
		"""
		mapData contains the following important information:
							Coordinates
							Elevation Information
		Sample:
										[[(2.1,0,5),1500],[...]]
										  /     \       \ 
									longtitude latitude elevation(in meter)
		Note: if more than one samples are in the same pixel on x-y plate, we take the highest point as the height.
		"""

		# Generating map from the data we get from web.  
		# Initially the map is contained with each pixiel together with a bool value True,which means all pixels are not occupied (neither by plane nor by land)
		# Note: we take the lowerleft point as origin.
		Status = "empty"
		# print(self._length)
		'''
		This part is commented for atc.py to work, there are still missing data here.
		'''
		# for i in range(self._length):
		# 	self._map.insert([])
		# 	for j in range(self._width):
		# 		self._map[i].insert([])
		# 		for k in range(self._height):
		# 			self._map[i][j].insert([Status])
		# # Then from mapData get the elevation info into the map.
		# for coordinate,elevation in mapData:
		# 	x = (abs(coordinate[0] - self._leftMost) * cos(coordinate[1]) * 6371000) // self._lengthResolution
		# 	y = (abs(coordinate[1] - self._lowerMost) * 6371000) // self._widthResolution
		# 	if elevation - self._minHeight - self._airportElevation > 0:
		# 		exceededHeight = elevation - self._minHeight - self._airportElevation
		# 		z = min(exceededHeight // self._heightResolution + 1,height)
		# 		for i in range(z):
		# 			self._map[x][y][i][0] = "occupied"

		# Next put the special areas into the map(areas where control tower takes over, usually 20000 meters from one end of the runway)
		'''
		This part is commented for atc.py to work, there are still missing data here.
		'''
		for r in range(self._numRunway):
			firstEnd,secondEnd = self._runwayLocations[r]
			x1 = abs(firstEnd[0] - self._leftMost) * cos(firstEnd[1]) * 6371000
			y1 = abs(firstEnd[1] - self._lowerMost) * 6371000
			x2 = abs(secondEnd[0] - self._leftMost) * cos(secondEnd[1]) * 6371000
			y2 = abs(secondEnd[1] - self._lowerMost) * 6371000
			direction = self._runwayDirections[r]
			tanValue = sinValue = cosValue = 0
			if direction[1] == 0:
				sinValue = 1
				cosValue = 0
			else:
				tanValue = direction[0] / direction[1]
				sinValue = tanValue / sqrt(1 + tanValue**2)
				cosValue = 1 / sqrt(1 + tanValue**2)
			x1 -= 20000 * cosValue
			y1 -= 20000 * sinValue
			x2 += 20000 * cosValue
			y1 += 20000 * sinValue
			x1 = x1 // self._widthResolution
			y1 = y1 // self._lengthResolution
			x2 = x2 // self._widthResolution
			y2 = y2 // self._lengthResolution
			for i in range(-1,2):
				for j in range(-1,2):
					self._map[x1 + i][y1 + j][0] = "handover"
					self._map[x1 + i][y1 + j][0].append("empty")
					self._map[x1 + i][y1 + j][0].append(1)
					self._map[x2 + i][y2 + j][0] = "handover"
					self._map[x2 + i][y2 + j][0].append("empty")
					self._map[x2 + i][y2 + j][0].append(2)
					# 1 stand for from south and west, 2 stand for from north and east

	# def notAbleToLand():
	# 	pass

	def getPlaneInfo(self,flightList):
		"""
		We get a sequence of flights info (a list of dictionaries) from input and put them in the map, once there's a error we will add a count to the penalty counter, and give an error.
		If a plane successfully enter handover region, return its data in the same formation to make it possible to pass it to control tower
		"""
		for data in flightList:
			plane = genericAirplane(data)
			direction = plane.direction
			departureCity = plane.departureCity
			longtitude,latitude = plane.position
			longtitude = longtitude * 3.14 / 180
			latitude = latitude * 3.14 / 180
			z = (plane.altitude - self._minHeight - self._airportElevation) // self._heightResolution + 1
			x = y = -1
			if longtitude > self._leftMost and longtitude < self._rightMost and latitude < self._upperMost and latitude > self._lowerMost:
				x = (abs(longtitude - self._leftMost) * cos(latitude) * 6371000) // self._lengthResolution
				y = (abs(latitude - self._lowerMost) * 6371000) // self._widthResolution
			if x > 0 and y > 0:
				if self._map[x][y][z][0] == "occupied":
					# this plane crashed
					self._crashCounter += 1
				elif self._map[x][y][z][0] == "empty":
					# safely add to the map
					self._map[x][y][z][0] = "occupied"
				elif self._map[x][y][z][0] == "handover":
					if self._map[x][y][z][1] == "empty":
						if departureCity == "CTU":
							pass
						else:
							pass
					elif self._map[x][y][z][1] == "occupied":
						pass

	def emptyMap(self):
		"""
		After checking in all info from the list, to avoid creating a new map on every iteration, use this method to empty the whole map for the next iteration,
		and this would not clear the penalty counters, but if needed, you can clear it in anotehr method.
		"""
		pass

	def clearCounters(self):
		"""
		Clear the penalty counters
		"""
		self._crashCounter = 0
		self._mislandingCounter = 0


class map(controlTower,approachControlArea):
	"""
	unite two classes for data transfering and dynamic analysis

	this class is not finished
	"""

	def __init__(self):
		# parameters needed are not determined yet
		pass

	def getDataFromFlightList(self,flightList):
		# get data from input flight list and put it into approach control area
		pass

	def getDataFromControlTower(self,flightList):
		#get data from  control tower and put them into approach control area
		pass
	def requestForLanding(self,flight,runwayNumber):
		# pass landing request from approach control area to control tower
		pass

	def emptyMap(self):
		# clear the map for next checking process
		pass