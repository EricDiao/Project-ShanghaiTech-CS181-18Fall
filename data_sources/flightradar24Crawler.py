#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Diao Zihao <hi@ericdiao.com>. All right reserved.

import requests

FR24_API_URL = "https://data-live.flightradar24.com/zones/fcgi/feed.js?bounds={},{},{},{}&faa=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=1&estimated=1&maxage=14400&gliders=1&stats=1"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"


def crawlFR24(border):
    """
    `crawlFR24(border)`

    `border = [(31.13, 102.28), (29.51, 102.28), (31.13, 106.22), (29.51, 106.22), ]`

    This function crawers realtime flight data from FlightRadar24.com within the border.
    Please be NOTE: because the data is from real world, some attribute may be missed.
    """
    longtitudeUpperLimit = max(
        border[0][0], border[1][0], border[2][0], border[3][0])
    longtitudeLowerLimit = min(
        border[0][0], border[1][0], border[2][0], border[3][0])
    latitudeUppperLimit = max(
        border[0][1], border[1][1], border[2][1], border[3][1])
    latitudelowerLimit = min(
        border[0][1], border[1][1], border[2][1], border[3][1])
    result = requests.get(FR24_API_URL.format(longtitudeUpperLimit, longtitudeLowerLimit,
                                              latitudelowerLimit, latitudeUppperLimit), headers={"User-Agent": USER_AGENT})
    airplanes = []
    if result.ok:
        result = result.json()
        for item in result:
            if isinstance(result[item], list):
                for i in range(len(result[item])):
                    if result[item][i] == '':
                        result[item][i] = None
                #print(result[item])
                thisPlane = {}
                if len(result[item]) >= 19:
                    thisPlane['longtitude'] = result[item][1]
                    thisPlane['latitude'] = result[item][2]
                    thisPlane['heading'] = result[item][3]
                    thisPlane['alititude'] = result[item][4]
                    thisPlane['groundSpeed'] = result[item][5]
                    thisPlane['squawk'] = result[item][6]
                    thisPlane['flightType'] = result[item][8]
                    thisPlane['registration'] = result[item][9]
                    thisPlane['depature'] = result[item][11]
                    thisPlane['destination'] = result[item][12]
                    thisPlane['flight'] = result[item][13]
                    airplanes.append(thisPlane)
    return airplanes


if __name__ == "__main__":
    border = [(31.13, 102.28), (29.51, 102.28),
              (31.13, 106.22), (29.51, 106.22), ]
    print(crawlFR24(border))
