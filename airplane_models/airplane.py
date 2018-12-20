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

    def __init__(self, flightType=None, flight=None, registration=None, depature=None, destination=None, eta=None, etd=None):
        self._type = flightType.upper()
        self._flight = flight.upper()
        # The flight number. Consists of two-character airline designator and a 1 to 4 digit number. For example, flight number CA981 stands for Air China flight number 981 (it departs Beijing's PEK and goes to New York's JFK). See https://en.wikipedia.org/wiki/Airline_codes#IATA_airline_designator for list of airline designator.
        # If there is no flight number for this flight (e.g. for private flight), use its egistration (of self._registrayion).
        self._registration = registration.upper()
        # In the ICAO format. For example, all chinese airplanes' registration has prefix `B` (with an optional dash)
        # and 4 characters (number and english letter) (for mainland China). e.g. B-123A.
        self._depatureCity = depature.upper()
        self._destination = destination.upper()
        # Above two are in the ICAO airport code format. For example, ZUUU for Chengdu/Shuangliu, ZSPD for Shanghai/Pudong.
        # see: https://en.wikipedia.org/wiki/List_of_airports_by_IATA_and_ICAO_code
        self._ETA = eta
        self._ETD = etd
        # Above two are in the UNIX timestamp format (We are CS student, right? And also we do not needs to deal with events before 1970-01-01 12:00, right?). e.g. (int) 15700000
        self._spec = {"maxSpeed": 101}
        # below are `dynamic` parameters that could change through time.
        self._heading = 0.0
        # range from 0.0 to 360.0 (in degree)
        self._longitude = 0.0
        self._latitude = 0.0
        # 经纬度。 In float format. e.g 31.12345
        self._alititude = 0.0
        # In meters.
        self._groundSpeed = 0.0
        # 海里。
        self._squawk = '7700'  # NOTE: this is a str.
        # If you wonder what is a `Squawk`, refer to https://en.wikipedia.org/wiki/Transponder_(aeronautics).

    def __repr__(self):
        # return "[{}] {} {} @ ({}, {}) - {}".format(self._squawk, self._registration, self._type, self._longitude, self._latitude, self._alititude)
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
        return self._type

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
    def postion(self):
        return (self._longitude, self._latitude)

    @postion.setter
    def postion(self, value):
        self._longitude = value[0]
        self._latitude = value[1]

    @property
    def heading(self):
        return self._heading

    @heading.setter
    def heading(self, value):
        if value < 0.0 or value > 360.0:
            raise ValueError
        self._heading = value

    @property
    def alititude(self):
        return self._alititude

def baseAirplaneTest():
    test = baseAirplane(flightType="A330", flight="Ca1999",
                            registration="b-6878", depature="PVG", destination="ctu")
    print("Testing class `baseAirplane`.")
    print(test)
    print("Getting values.")
    print(test.groundSpeed, test.getSpec())
    test.groundSpeed = 100
    print("groundSpeed set to {}".format(test.groundSpeed))
    try:
        test.groundSpeed = -1
    except ValueError:
        print("Negative speed test passed.")
    print('Test passed.')

if __name__ == "__main__":
    baseAirplaneTest()
