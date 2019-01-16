#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Diao Zihao <hi@ericdiao.com>. All right reserved.

import simplejson
from math import sin, cos, tan


class baseAirplane:
	"""
	Base airplane type for CS 181 Project. Provides basic interfaces for creating a new airplane.

	Please DO NOT use this in practice. See the comments below for more information.
	"""

	def __init__(self, flightType=None, flight=None, registration=None, depature=None, destination=None, eta=None, etd=None, 
				heading=0.0,longitude = 0.0,latitude = 0.0, altitude = 0.0,groundSpeed = 0.0,squawk = '7700',prior = 0):
		self._type = flightType.upper()
		#There are cases that the flight information remain None for an airplane. Hang
		if flight != None:
			self._flight = flight.upper()
		# The flight number. Consists of two-character airline designator and a 1 to 4 digit number. For example, flight number CA981 stands for Air China flight number 981 (it departs Beijing's PEK and goes to New York's JFK). See https://en.wikipedia.org/wiki/Airline_codes#IATA_airline_designator for list of airline designator.
		# If there is no flight number for this flight (e.g. for private flight), use its egistration (of self._registrayion).
		self._registration = registration.upper()
		# In the ICAO format. For example, all chinese airplanes' registration has prefix `B` (with an optional dash)
		# and 4 characters (number and english letter) (for mainland China). e.g. B-123A.

		#There are cases that the depature or destination information remain None for an airplane. Hang
		if depature != None:
			self._depatureCity = depature.upper()
		if destination != None:
			self._destination = destination.upper()
		# Above two are in the ICAO airport code format. For example, ZUUU for Chengdu/Shuangliu, ZSPD for Shanghai/Pudong.
		# see: https://en.wikipedia.org/wiki/List_of_airports_by_IATA_and_ICAO_code
		self._ETA = eta
		self._ETD = etd
		# Above two are in the UNIX timestamp format (We are CS student, right? And also we do not needs to deal with events before 1970-01-01 12:00, right?). e.g. (int) 15700000
		self._spec = {"maxSpeed": 500, "ceiling": 6000}
		# below are `dynamic` parameters that could change through time.
		# self._heading = 0.0
		self.heading = heading
		# range from 0.0 to 360.0 (in degree)
		# self._longitude = 0.0
		# self._latitude = 0.0
		self.position = [longitude,latitude]
		# In float format. e.g 31.12345
		# self._altitude = 0.0
		self.altitude = altitude
		# In meters.
		# self._groundSpeed = 0.0
		self.groundSpeed = groundSpeed
		# hm
		self._squawk = squawk  # NOTE: this is a str.
		# If you wonder what is a `Squawk`, refer to https://en.wikipedia.org/wiki/Transponder_(aeronautics).
		self.priority = prior

	def __repr__(self):
		# return "[{}] {} {} @ ({}, {}) - {}".format(self._squawk, self._registration, self._type, self._longitude, self._latitude, self._altitude)
		return "{}\n{}-{}\n{}\n{}\n{}".format(self._flight, self._depatureCity, self.destination, self.type, self._registration, self.squawk)

	@property
	def registration(self):
		return self._registration

	@property
	def type(self):
		return self._type

	def getSpec(self, arg=None):
		if arg:
			return self._spec[arg]
		return self._spec

	@property
	def flight(self):
		return self._flight

	@property
	def depatureCity(self):
		return self._depatureCity

	@property
	def destination(self):
		return self._destination

	@property
	def squawk(self):
		return self._squawk

	@property
	def ETD(self):
		return self._ETD

	@property
	def ATD(self):
		pass

	@property
	def ETA(self):
		return self._ETA

	@property
	def groundSpeed(self):
		return self._groundSpeed

	@groundSpeed.setter
	def groundSpeed(self, value):
		if value > self._spec['maxSpeed'] or value < 0:
			raise ValueError
		self._groundSpeed = value

	def getAirSpeed(self, airSpeed, airSpeedHeading):
		pass
		# TODO: calculate speed.

	@property
	def position(self):
		return (self._longitude, self._latitude)

	@position.setter
	def position(self, value):
		longitude = value[0]
		latitude = value[1]
		if abs(longitude) > 180.0 and abs(latitude) > 90.0:
			raise ValueError
		self._longitude = longitude
		self._latitude = latitude

	@property
	def heading(self):
		return self._heading

	@heading.setter
	def heading(self, value):
		if value < 0.0 or value > 360.0:
			raise ValueError
		self._heading = value

	@property
	def altitude(self):
		return self._altitude

	@altitude.setter
	def altitude(self, value):
		if value > self._spec['ceiling']:
			raise ValueError
			# TODO: specify a certain error for that.
		self._altitude = value

	def takeAction(self, actionParam):
		pass
		# TODO: waiting for the environment.


class genericAirplane(baseAirplane):
	"""
	`genericAirplane(flightType=None, flight=None, registration=None, depature=None, destination=None, eta=None, etd=None)`

	This is the default consturctor of an Airplane model.

	The `flightType` specify the model of the consturcted airplane. The
	constuctor will look for the corresponding `json` file in this directory
	and load it to self._spec.
	"""

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self._getSpecFromFile()

	def _getSpecFromFile(self):
		fileName = "{}{}.json".format("./models/", self._type)
		with open(fileName) as f:
			self._spec = simplejson.load(f)


def baseAirplaneTest():
	print("Testing class `baseAirplane`.")
	test = baseAirplane(flightType="A330", flight="Ca1999",
						registration="b-6878", depature="PVG", destination="ctu")
	print(test)
	print(test.__dict__)
	old_val = test.__dict__
	try:
		test.postion = (181.0, 91.0)
		print("Postion test failed.")
	except ValueError:
		print("Postion test passed.")
	try:
		test.heading = 361.0
		print("Heading test failed.")
	except ValueError:
		print("Heading test passed.")
	try:
		test.altitude = 12501
		print("Ceiling test failed.")
	except ValueError:
		print("Ceiling test passed.")
	assert test.__dict__ == old_val
	print("All test passed.")


def genericAirplaneTest():
	print("Testing class `genericAirplane`.")
	test = genericAirplane(flightType="A320", flight="Ca1999",
						   registration="b-6878", depature="PVG", destination="ctu")
	print(test)
	print(test.__dict__)
	old_val = test.__dict__
	
	try:
		test.postion = (181.0, 91.0)
		print("Postion test failed.")
	except ValueError:
		print("Postion test passed.")
	try:
		test.heading = 361.0
		print("Heading test failed.")
	except ValueError:
		print("Heading test passed.")
	try:
		test.altitude = 12501
		print("Ceiling test failed.")
	except ValueError:
		print("Ceiling test passed.")
	assert test.__dict__ == old_val
	print("All test passed.")


if __name__ == "__main__":
	baseAirplaneTest()
	genericAirplaneTest()
