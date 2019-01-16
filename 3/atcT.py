#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Diao Zihao <hi@ericdiao.com>. All right reserved.

import time, logging
from multiprocessing import Process, Queue
from data_sources.flightradar24Crawler import crawlFR24, crawlFR24MultiprocessingWrapper
from airplane_models.airplane import baseAirplane
from map_models.newMap import Map
from QlearningAgent.qlearningAgent import QLearningAgent
import random
from util import Counter


def data_consumer(queue, interval, space,allPlanes,allPlanesLocation):
    """
    `data_consumer(queue, interval)`

    This is an EXAMPLE of the multiprocessing data consumer.
    You may write your own one and replace `data_consumer` in the following "main function".
    """
    while True:
        data = queue.get()
        logging.info("Data consumer: get data with timestamp {}.")
        # print("get data: ")#,end=''
        # print(data)
        # print("LeftMost:",space._leftMost)
        timeStamp = list(data.keys())
        timeStamp = timeStamp[0]
        planes = list(data.values())
        planes = planes[0]
        planes = [{
        "longitude": 30.4537,
        "latitude": 103.7644,
        "heading": 201,
        "altitude": 6700,
        "groundSpeed": 223,
        "squawk": "5316",
        "flightType": "A321",
        "registration": "B-6386",
        "depature": "CGQ",
        "destination": "CTU",
        "flight": "CA4190"},
    {
        "longitude": 30.3495,
        "latitude": 103.7935,
        "heading": 112,
        "altitude": 5350,
        "groundSpeed": 192,
        "squawk": "6371",
        "flightType": "A333",
        "registration": "B-1059",
        "depature": "TNA",
        "destination": "CTU",
        "flight": "8L9764"
    },
    {
        "longitude": 30.5952,
        "latitude": 103.8303,
        "heading": 202,
        "altitude": 8725,
        "groundSpeed": 251,
        "squawk": "7055",
        "flightType": "A319",
        "registration": "B-6047",
        "depature": "INC",
        "destination": "CTU",
        "flight": "CA4232"
    }]
        
        # states = filter(lambda state : len(space.getPossibleActions(state)) > 0,space.getStates())
        # states.sort()
        # if it is a plane within altitude 1000-6000 and preparing to land at CTU, then we put it into plane list.
        for i in planes:
            # print(i)
            if not i['flight'] in allPlanes.keys():
                if (i['destination'] == "CTU") & ((i['altitude']-space._airportElevation) < 6000) & ((i['altitude']-space._airportElevation) > 1000) :
                    # print(i['altitude'])
                    agent = QLearningAgent(baseAirplane(i['flightType'],i['flight'],i['registration'],i['depature'],i['destination'],None,None,
                        i['heading'],i['latitude'],i['longitude'],i['altitude']-space._airportElevation,i['groundSpeed'],i['squawk']),space)
                    allPlanes[i['flight']] = agent
                    #store the state of all plane as another dict for convenience
                    allPlanesLocation[i['flight']] = [agent.X,agent.Y,agent.Z]
                    # agent.stateReward = space._map[agent.X][agent.Y][agent.Z]
        # creat a temporary agent to do the training
        # tempAgent = QLearningAgent(baseAirplane(flightType="A330", flight="Ca1999",
        #                 registration="b-6878", depature="PVG", destination="ctu"),space)
        
        
        # because all agents will use the same q value except a bit difference, 
        # so store the result in space(global map)
        # space.values = tempAgent.values.copy()
        # change the value of the states where a plane is in the state
        # because planes within one state is a collision
        
        for i in allPlanesLocation.values():
            for j in space.values.keys():
                if j[2] == str(i):
                    space.tempValue[j] = space.values[j]
                    space.values[j] = -100
                    # print('plane:',j)
            print(i)
            space.tempValue[str(i)] = space._map[i[0]][i[1]][i[2]]
            # print('tempvalue:',str(i),space._map[i[0]][i[1]][i[2]])
            space._map[i[0]][i[1]][i[2]] = -100
        tempPlaneLocation = allPlanesLocation.copy()
        # for all planes decide where they are going next
        print('start training')
        xxx = 0
        for i in allPlanes.keys():
            xxx += 1
            print('plane:',i)
            currentAgent = allPlanes[i]
            currentAgent.values = space.values.copy()  
            currentState =  [currentAgent.X,currentAgent.Y,currentAgent.Z]
            for j in space.values.keys():
                if j[2] == str(currentState):
                    currentAgent.values[j] = space.tempValue[j]
            space._map[currentAgent.X][currentAgent.Y][currentAgent.Z] = space.tempValue[str(currentState)]
            lastExperience = None
            startState = [(currentAgent.kmX,currentAgent.kmY,currentAgent.kmZ),\
                (currentAgent.plane.heading,currentAgent.plane.groundSpeed)]
            for ccc in range(10000):
                currentAgent.computeValueFromQValues(startState)
                PossibleAction = space.getPossibleActions(startState)
                actions = []
                for action in PossibleAction:
                    if (space.getPossibleActions(space.getNextState(startState,action)) != []):
                        actions.append(action)
                if(xxx == 1):
                    print('PossibleAction:',PossibleAction)
                    print('actions:',actions)
                action = currentAgent.computeActionFromQValues(startState)
                # action = random.choice(actions)
                if(xxx == 1):
                    print(action)
                endState = space.getNextState(startState,action)
                # print("endState:",endState)
                reward = currentAgent.getReward(endState)
                lastExperience = (startState, action, endState, reward)
                currentAgent.update(*lastExperience)
                startState = endState
                tempX, tempY = space.XYInDistToCoordinate((endState[0][0],endState[0][1]))
                if(xxx == 1):
                    print('currentState:',tempX,tempY,endState[0][2],endState[1],ccc)
            startState = [(currentAgent.kmX,currentAgent.kmY,currentAgent.kmZ),\
            (currentAgent.plane.heading,currentAgent.plane.groundSpeed)]
            action = currentAgent.computeActionFromQValues(startState)  
            endState = currentAgent.getNextState(startState,action)
            space._map[currentAgent.X][currentAgent.Y][currentAgent.Z] = -100
            currentAgent.kmX,currentAgent.kmY,currentAgent.kmZ = endState
            currentAgent.X, currentAgent.Y = XYInDistToCoordinate((currentAgent.kmX,currentAgent.kmY))
            currentAgent.Z = currentAgent.kmZ
            allPlanesLocation[i] = endState[0]
            allPlanes[i]['groundSpeed'] = endState[1][1]
            allPlanes[i]['heading'] = endState[1][0]
            print('plane&state:',i,endState)
            # TODO: find out what is wrong
            # Try to delete the plane once it is 20km from one head of the runway, but failed
            # since it 4am now, so there is no real time data for me to do the test
            if (list(endState[0]) == list(space.runwayLocationCoordinate1)+[0]) or \
            (list(endState[0]) == list(space.runwayLocationCoordinate2)+[0]):
                print('landed:',allPlanes.pop(i))
                print('landed:',allPlanesLocation.pop(i))
                space._map[endState[0][0]][endState[0][1]][0] = 20
        for i in tempPlaneLocation.values():
            space._map[i[0]][i[1]][i[2]] = space.tempValue[str(i)]
            # print('newvalue:',str(i),space._map[i[0]][i[1]][i[2]])
        space.tempPlaneLocation = Counter()

        '''
        I use both the initial value of the nextState and the Q value of the (state,action,nextState)
        to decide which action to do next. 
        This is because there are too many states, and we are not able to get a reliable q value
        even after 100000 trails
        '''
        # print(space.values.keys())


        # print(Map.x,Map.y,Map.z)
        # print(Map.plane.keys())
        # find collision 

            # Under what situations do we need to make an instruction?
            # collistion / no road remain /
            # Under what situations does the plane make an request to tower?
            # Landing
            # decide weather there are collisions now or future.
            # input arguments: 
            # print(i['heading'])
            # print(newPlane.heading)
        time.sleep(interval)


if __name__ == "__main__":
    logging.basicConfig(filename='atc.log',
                        format='%(levelname)s:%(asctime)s - %(message)s', level=logging.INFO)
    border = [(31.13, 102.28), (29.51, 102.28),
              (31.13, 106.22), (29.51, 106.22), ]  # This shall be passed in by sys.argv.
    # Map = map(controlTower(),approachControlArea())
    # Map = approachControlArea(29.51,31.13,106.22,102.28)
    space = Map()
    print(space.runwayLocationCoordinate1,space.runwayLocationCoordinate2)
    print(len(space._map),len(space._map[0]),len(space._map[0][0]))
    allPlanes = Counter()
    allPlanesLocation = Counter()
    # print(space.End)
    logging.info("Artifical Idiot ATC started.")
    data_queue = Queue()
    logging.info("Mutiprocessing: data queue initialized.")
    data_consumer = Process(target=data_consumer, args=(data_queue, 10, space,allPlanes,allPlanesLocation))
    logging.info("Mutiprocessing: data consumer initialized.")
    data_provider = Process(
        target=crawlFR24MultiprocessingWrapper, args=(border, data_queue, 15,))
    logging.info("Mutiprocessing: data provider initialized.")
    data_provider.start()
    logging.info("Mutiprocessing: data provider started.")
    data_consumer.start()
    logging.info("Mutiprocessing: data consumer started.")
    logging.info("ATC initialized.")
