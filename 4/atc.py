#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Diao Zihao <hi@ericdiao.com>. All right reserved.

import time, logging
from multiprocessing import Process, Queue
from data_sources.flightradar24Crawler import crawlFR24, crawlFR24MultiprocessingWrapper
from airplane_models.airplane import baseAirplane
from map_models.map import approachControlArea
from QlearningAgent.qlearningAgent import tran, Map, Directions,QLearningAgent
import random
import simplejson as json
from util import Counter
from math import ceil


def data_consumer(queue, interval, space):
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
		
		# states.sort()
		# if it is a plane within altitude 1000-6000 and preparing to land at CTU, then we put it into plane list.
		for i in planes:
			# print(i)
			if not i['flight'] in space.plane.keys():#(i['destination'] == "CTU") & 
				if (i['altitude'] < 6000) & (i['altitude'] > 1000) :
					plane = baseAirplane(i['flightType'],i['flight'],i['registration'],i['depature'],i['destination'],None,None,
						i['heading'],i['longitude'],i['latitude'],i['altitude'],i['groundSpeed'],i['squawk'])
					space.plane[i['flight']] = plane
					#store the state of all plane as another dict for convenience
					positionX, positionY = space.LongLaToXY(plane.position)
					positionZ = space.AltToZ(plane.altitude)
					space.planeLocation[i['flight']] = [positionX,positionY,positionZ]
		length = [1,2,3,4,5,6,7,8,9,10]
		for i in length:
			print(str(i))
			# print('start')
			# states = space.getStates(num)
			# print('end')
			with open(str(i),'w') as f:
				# print('start')
				new_data = space.getStates(i)
				jsData = json.dumps(new_data,indent = 4)
				f.write(jsData)
				f.write('\n')
				f.close()
		# # agent.stateReward = space.whole[agent.X][agent.Y][agent.Z]
		# # creat a temporary agent to do the training
		# Qagent = QLearningAgent(space.plane,space.planeLocation,space)
		# # tempAgent = QLearningAgent(baseAirplane(flightType="A330", flight="Ca1999",
		#                 # registration="b-6878", depature="PVG", destination="ctu"),space)
		# # lastExperience = None
		# for _ in range(10):
		#     startState = random.choice(states)
		#     print(startState)

		#                 action = random.choice(space.getLegalActions(startState))
		#                 endState = Qagent.getNextState(startState,action)
		#                 reward = Qagent.getReward(endState)
		#                 lastExperience = (startState, action, endState, reward)
		#                 Qagent.update(*lastExperience)
		#             space.agent = Qagent
		# agent = space.agent
		# startState = [(space.LongLaToXY(plane.position)+[space.AltToZ(plane.altitude)]) for plane in agent.planes.values()]
		# startState.sort()
		# print(startState)
		# action = agent.computeActionFromQValues(startState)
		# endState = agent.getNextState(startState,action)
		# for i in space.plane.values():
		#     order = startState.index((i.position+[i.altitude]))
		#     tempAction = action[order]
		#     nextState = endState[order]
		#     Long,Lat, alt = agent.getPosition(startState,action)
		#     i.position = [Lat,Long]
		#     i.altitude = alt


		# because all agents will use the same q value except a bit difference, 
		# so store the result in space(global map)
		# space.values = tempAgent.values.copy()
		# change the value of the states where a plane is in the state
		# because planes within one state is a collision
		# print(space.x,space.y,space.z)
		# for i in space.planeLocation.values():
		#     for j in space.values.keys():
		#         if j[2] == str(i):
		#             space.tempValue[j] = space.values[j]
		#             space.values[j] = -100
		#             # print('plane:',j)
		#     print(i)
		#     space.tempValue[str(i)] = space.whole[i[0]][i[1]][i[2]]
		#     # print('tempvalue:',str(i),space.whole[i[0]][i[1]][i[2]])
		#     space.whole[i[0]][i[1]][i[2]] = -100
		# tempPlaneLocation = space.planeLocation.copy()
		# # for all planes decide where they are going next
		# for i in space.plane.keys():
		#     currentAgent = space.plane[i]
		#     currentAgent.values = space.values.copy()  
		#     currentState =  [currentAgent.X,currentAgent.Y,currentAgent.Z]
		#     for j in space.values.keys():
		#         if j[2] == str(currentState):
		#             currentAgent.values[j] = space.tempValue[j]
		#     space.whole[currentAgent.X][currentAgent.Y][currentAgent.Z] = space.tempValue[str(currentState)]
		#     action = currentAgent.computeActionFromQValues(currentState)  
		#     endState = currentAgent.getNextState(currentState,action)  
		#     space.whole[currentAgent.X][currentAgent.Y][currentAgent.Z] = -100
		#     currentAgent.X,currentAgent.Y,currentAgent.Z = endState
		#     space.planeLocation[i] = endState
		#     print('plane&location:',i,endState)
		#     # TODO: find out what is wrong
		#     # Try to delete the plane once it is 20km from one head of the runway, but failed
		#     # since it 4am now, so there is no real time data for me to do the test
		#     if (endState == [40,67,0]) or (endState == [42,68,0]):
		#         print('landed:',space.plane.pop(i))
		#         print('landed:',space.planeLocation.pop(i))
		# for i in tempPlaneLocation.values():
		#     space.whole[i[0]][i[1]][i[2]] = space.tempValue[str(i)]
		#     # print('newvalue:',str(i),space.whole[i[0]][i[1]][i[2]])
		# space.tempPlaneLocation = Counter()

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
	print(space.End)
	logging.info("Artifical Idiot ATC started.")
	data_queue = Queue()
	logging.info("Mutiprocessing: data queue initialized.")
	data_consumer = Process(target=data_consumer, args=(data_queue, 10, space))
	logging.info("Mutiprocessing: data consumer initialized.")
	data_provider = Process(
		target=crawlFR24MultiprocessingWrapper, args=(border, data_queue, 15,))
	logging.info("Mutiprocessing: data provider initialized.")
	data_provider.start()
	logging.info("Mutiprocessing: data provider started.")
	data_consumer.start()
	logging.info("Mutiprocessing: data consumer started.")
	logging.info("ATC initialized.")
