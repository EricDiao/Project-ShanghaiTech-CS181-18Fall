#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Diao Zihao <hi@ericdiao.com>. All right reserved.


def getCenterFromBorder(border):
    """
    This function takes in a list of four tuples representing the border points
    of a square aera and return a tuple representing its center point.
    """
    longtitude = 0.0
    latitude = 0.0
    for p in border:
        longtitude += p[0]
        latitude += p[1]
    return (longtitude/4, latitude/4)
