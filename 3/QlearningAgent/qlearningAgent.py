import random, traceback, sys, os
sys.path.append("..")
from util import Counter,manhattanDistance
from airplane_models.airplane import baseAirplane
from map_models.newMap import Map
from math import sin,cos,sqrt,pi,acos

# def tran(a):
#     # print('a:',a)
#     if a == str(Directions.NORTH):
#         a = [0,1,0]  #y+1
#     if a == str(Directions.SOUTH):
#         a = [0,-1,0]  #y-1
#     if a == str(Directions.EAST):
#         a = [1,0,0]    #x-1
#     if a == str(Directions.WEST):
#         a = [-1,0,0]    #x+1
#     if a == str(Directions.UP):
#         a = [0,0,1]      #z+1
#     if a == str(Directions.DOWN):
#         a = [0,0,-1]     #z-1
#     if a == str(Directions.STOP):
#         a = [0,0,0]
#     # print('a:',a)
#     return a




# class Map:
#     def __init__(self):
#         # original: (30.563688,103.940061),(30.519631,103.936683)
#         # vertical: (30.563688,103.951040),(30.519631,103.936683) 0.003139
#         # vertical + 20km: (30.560549,103.951040),(30.516492,103.936683)
#         # (30.559156,103.954450)
#         # runway1 = (30.563688,103.936922)
#         # runway2 = (30.519631,103.933544)
#         runway1 = (30.560549,103.951040)
#         runway2 = (30.516492,103.936683)
#         way1 = (29.51,103.836184)
#         way2 = (29.51,104.051539)
#         self.Left= 102.28
#         self.Right= 106.22
#         self.Down = 29.51 
#         self.Up= 31.13
#         self.R = 6371000
#         self.x,self.y = self.LongLaToXY([self.Right,self.Up])
#         self.z = int((6000-1000)//1000)
#         # self.z = 2
#         self._map = [[[(4-i) for i in range(self.z)] for _ in range(self.y)] for _ in range(self.x)]
#         for i in range(self.x):
#             for j in range(self.y):
#                 self._map[i][j][0] = -100
#         # print(len(self._map),len(self._map[0]),len(self._map[0][0]))
#         positionR1 = self.LongLaToXY(runway1)
#         positionR2 = self.LongLaToXY(runway2)
#         self._map[positionR1[0]][positionR1[1]][0] = 200
#         self._map[positionR2[0]][positionR2[1]][0] = 200
#         positionW1 = self.LongLaToXY(way1)
#         positionW2 = self.LongLaToXY(way2)
#         print(positionW1,positionW2)
#         self.End = [positionR1,positionR2]
#         for i in range(positionR1[0]+1):
#             self._map[i][positionR1[1]][1] = 100+2*(i-positionR1[0])
#         for i in range(positionR2[0]+1):
#             self._map[i][positionR2[1]][1] = 100+2*(i-positionR2[0])
#         for i in range(self.x):
#             self._map[i][positionW1[1]][1] = 10-0.1*i
#             self._map[i][positionW2[1]][1] = 10-0.1*i
#         # print(self._map)
#         # print('runway:',self.End)
#         # print('dis:',self.LongLaToXY(way1),self.LongLaToXY(way2))

#         self.plane = Counter()
#         self.planeLocation = Counter()
#         self.values = Counter()
#         self.tempValue = Counter()

#     def LongLaToXY(self,position):
#         C = sin(self.Left)*sin(self.Left)*cos(position[0]-self.Down)+cos(self.Left)*cos(self.Left)
#         positionX = self.R*pi/180*acos(C)
#         C = sin(self.Left)*sin(position[1])*cos(self.Down-self.Down)+cos(self.Left)*cos(position[1])
#         positionY = self.R*pi/180*acos(C)

#         return [int(positionX//2750+1),int(positionY//2750+1)]

#     def AltToZ(self,alt):
#         # print(alt)
#         return int((alt-1000)//1000+1)
#     def getStates(self):
#         states = []
#         for i in range(self.x):
#             for j in range(self.y):
#                 for k in range(self.z):
#                     states.append([i,j,k])
#         return states

#     def getPossibleActions(self,state):
#         if state == self.End:
#             return []
#         x,y,z = state
#         actions = []
#         if x > 0 :  
#             actions.append(Directions.WEST)
#         if x < self.x:
#             actions.append(Directions.EAST)
#         if y > 0 :
#             actions.append(Directions.SOUTH)
#         if y < self.y:
#             actions.append(Directions.NORTH)
#         if z > 0 :
#             actions.append(Directions.DOWN)
#         if z < self.z:
#             actions.append(Directions.UP)
#         actions.append(Directions.STOP)
#         return actions

# # class State():
# #     def __init__(self,x=0,y=0,z=0):
# #         self.x = x
# #         self.y = y
# #         self.z = z
# class Directions:
#     # NORTH = 'North'  #y+1
#     # SOUTH = 'South'  #y-1
#     # EAST = 'East'    #x-1
#     # WEST = 'West'    #x+1
#     # UP = 'Up'        #z+1
#     # DOWN = 'Down'    #z-1
#     NORTH = [0,1,0]  #y+1
#     SOUTH = [0,-1,0]  #y-1
#     EAST = [1,0,0]    #x-1
#     WEST = [-1,0,0]    #x+1
#     UP = [0,0,1]      #z+1
#     DOWN = [0,0,-1]     #z-1
#     STOP = [0,0,0]


class QLearningAgent:
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getPossibleActions(state)
          which returns legal actions for a state
    """
    def __init__(self,plane,Map = None,actionFn = None, alpha=0.5, gamma=0.95,epsilon = 0.1):
        "You can initialize Q-values here..."
        # if actionFn == None:
        #     actionFn = lambda state: state.getPossibleActions()
        self.running = 0
        self.actionFn = actionFn
        self.plane = plane
        self.Map = Map
        # self.episodesSoFar = 0
        # self.accumTrainRewards = 0.0
        # self.accumTestRewards = 0.0
        # self.numTraining = int(numTraining)
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)
        self.values = Counter()
        self.oldValues = Counter()
        # print(plane.position,plane.altitude)
        self.X ,self.Y = self.Map.XYInDistToCoordinate(self.Map.longLaToXYInDist(plane.position))
        self.Z = int((plane.altitude-1000)//self.Map._heightResolution)
        self.kmX,self.kmY = self.Map.longLaToXYInDist(plane.position)
        self.kmZ = plane.altitude

    # def getPossibleActions(self,state):
    #     if state == self.Map.End:
    #         return []
    #     x,y,z = state
    #     actions = []
    #     if x > 0 :  
    #         actions.append(Directions.WEST)
    #     if x < (self.Map.x-1):
    #         actions.append(Directions.EAST)
    #     if y > 0 :
    #         actions.append(Directions.SOUTH)
    #     if y < (self.Map.y-1):
    #         actions.append(Directions.NORTH)
    #     if z > 0 :
    #         actions.append(Directions.DOWN)
    #     if z < (self.Map.z-1):
    #         actions.append(Directions.UP)
    #     return actions

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        # print(self.values.keys())
        return self.oldValues[(str(state),str(action))]
        #state contains: (position_x, position_y, altitude, heading, speed]
        #action:(heading,speed, altitude)
        util.raiseNotDefined()

    def getReward(self,nextState):
        # if state == self.grid.terminalState:
        #     return 0.0
        # print('next:',nextState)
        # ((x, y, z), (h, s))
        a = nextState
        # print('nextState:',a)
        # print('a:',a[0][0],a[0][1])
        position = self.Map.XYInDistToCoordinate([a[0][0],a[0][1]])
        z = int((a[0][2]-1000)//self.Map._heightResolution)
        # print(position,z)
        rewardS = (150-a[1][1])/4
        # print(x,y,z)
        cell = self.Map._map[position[0]][position[1]][z]
        rewardT = 0
        rewardD = -min(manhattanDistance(list(self.Map.runwayLocationCoordinate1)+[0],list(position)+[z]),manhattanDistance(list(self.Map.runwayLocationCoordinate2)+[0],list(position)+[z]))
        if (position == self.Map.runwayLocationCoordinate1) or(position == self.Map.runwayLocationCoordinate2) and (z == 0):
            if (abs(a[1][0]) < 15) and (a[1][1] < 130):
                rewardT = self.Map._map[position[0]][position[1]][0]
        # print('reward:',x,y,z,self.Map._map[x][y][z])
        return (rewardS +cell+rewardT+rewardD/(5+z/5))
        # return self.livingReward

    # def getNextState(self,startState,action):
    #     s = startState
    #     a = action
    #     if type(startState) == type('a'):
    #         s = list(map(int,startState[1:-1].split(', ')))
    #     if type(action) == type('a'):
    #         a = list(map(int,action[1:-1].split(', ')))


    #     nextState = [s[0]+a[0],s[1]+a[1],s[2]+a[2]]
    #     # print(nextState)
    #     reward = self.getReward(nextState)
    #     return nextState

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        # print(state)
        actions = self.Map.getPossibleActions(state)
        # actions = []
        if len(actions) != 0:
            vals = []
            for action in actions:
                nextState = self.Map.getNextState(state,action)
                a = nextState
                #print('nextState:',a)
                #print('a:',a[0][0],a[0][1])
                position = self.Map.XYInDistToCoordinate([a[0][0],a[0][1]])
                z = int((a[0][2]-1000)//self.Map._heightResolution)
                # print('computeValueFromQValues:',a,position,z)
                vals.append(self.getQValue(state,action)+self.Map._map[position[0]][position[1]][z])
            return max(vals)
        return 0.0
        util.raiseNotDefined()

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        MainDict = self.values.keys()
        Action = []
        Max = []
        nextStates = []
        actions = self.Map.getPossibleActions(state)
        # print('actions:',actions)
        for action in actions:
            nextState = self.Map.getNextState(state,action)
            reward = self.getReward(nextState)
            self.update(state,action,nextState,reward)
            a = nextState
            position = self.Map.XYInDistToCoordinate([a[0][0],a[0][1]])
            z = int((a[0][2]-1000)//self.Map._heightResolution)
            # print('nextState:',position,z,nextState)
            # print(self.Map.getPossibleActions(nextState))
            if self.Map.getPossibleActions(nextState) != []:
                Action.append(action)
                nextStates.append([nextState,self.Map._map[position[0]][position[1]][z]])
                Max.append(self.getQValue(state,action)+self.Map._map[position[0]][position[1]][z])
        if self.running == 1:
            print('action:',Action)
            print('Max:',Max)
            self.running = 0

        # for i in MainDict:
        #     # print(i[0],str(state))
        #     if i[0] == str(state):
        #         # print(i)
        #         # print('aaaa:',i[0],i[1])
        #         nextState = self.Map.getNextState(eval(i[0]),eval(i[1]))
        #         a = nextState
        #         position = self.Map.XYInDistToCoordinate([a[0][0],a[0][1]])
        #         z = int((a[0][2]-1000)//self.Map._heightResolution)
        #         # print('nextState:',position,z,nextState)
        #         # print(self.Map.getPossibleActions(nextState))
        #         if self.Map.getPossibleActions(nextState) != []:
        #             Action.append(b)
        #             nextStates.append([nextState,self.Map._map[position[0]][position[1]][z]])
        #             Max.append(self.getQValue(i[0],i[1])+self.Map._map[position[0]][position[1]][z])


        # return random.choice(Action)
        # print(nextStates,)
        # print(Max)
        if Max == []:
            actions = self.Map.getPossibleActions(state)
            if actions == []:
                return None
            return random.choice(actions)
        # if random.random() < self.epsilon:
        #     return random.choice(Action)
        # else:
        return Action[Max.index(max(Max))]
        util.raiseNotDefined()

        # return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        # print(nextState)
        newSample = reward+ self.discount*self.computeValueFromQValues(nextState)
        self.values[(str(state),str(action))] = (1-self.alpha)*self.oldValues[(str(state),str(action))] + (self.alpha*newSample)
        return newSample
        util.raiseNotDefined()

    # def getPolicy(self, state):
    #     return self.computeActionFromQValues(state)

    # def getValue(self, state):
    #     return self.computeValueFromQValues(state)

def qlearningTest():
    print("Testing class qlearning")
    test = baseAirplane(flightType="A330", flight="Ca1999",
                        registration="b-6878", depature="PVG", destination="ctu")
    agent = QLearningAgent(test)
    space = Map()
    # print(space.x,space.y,space.z)
    agent.Map = space
    # print('End:',space._map[1][1][1])
    # print(agent.Map.getStates())
    states = filter(lambda state : len(space.getPossibleActions(state)) > 0,space.getStates())
    states.sort()
    # exit()
    randObj = random.sample(states, 1)
    print(randObj)
    # print(len(space._map))
    lastExperience = None
    space.plane[agent.plane.flight] = agent
    # End = [1,1,1]
    # count = 0
    for _ in range(1000):
        #add all planes position to the map
        # for key in space.plane.keys():
        #     s = space.plane[key].state
        #     space._map[s[0]][s[1]][s[2]] = -100
        startState = random.choice(states)
        # print(startState)
        action = random.choice(agent.getPossibleActions(startState))
        endState = agent.getNextState(startState,action)
        reward = agent.getReward(endState)
        lastExperience = (startState, action, endState, reward)
        agent.update(*lastExperience)
    # print(space._map)
    # print(agent.values)
    # print(space._map[12][29][3])
    # for i in agent.values.keys():
        # if i[0] == str([1,1,0]):
        # print(i,agent.values[i])
    # for _ in range(10):    
    #     # for each plane find next step 
    #     for key in space.plane.keys():
    #         currentAgent = space.plane[key]
    #         s = currentAgent.state
    #         #remove self from the map
    #         if s != space.End:
    #             space._map[s[0]][s[1]][s[2]] = 0
    #         else:
    #             space._map[s[0]][s[1]][s[2]] = 100
    #         space.plane[key]
    #         a = tran(currentAgent.computeActionFromQValues(s))
    #         # print(s+a)
    #         nextState = [s[0]+a[0],s[1]+a[1],s[2]+a[2]]
    #         currentAgent.update(s,a,nextState,1)
    #         currentAgent.state = nextState
            # print("current:",currentAgent.state)

    # print(agent.plane.flight)
    # print(test.altitude)


if __name__ == "__main__":
    # Map = approachControlArea(29.51,31.13,106.22,102.28,5500,5500,2)
    

    # C = sin(MLatA)*sin(MLatB)*cos(MLonA-MLonB) + cos(MLatA)*cos(MLatB)
    # DistanceY = R*math.acos(C)*Pi/180
    # print('DistanceY:',DistanceY)

    # [[(30.563688,103.940061),(30.593320,103.953838)],[(30.519631,103.936683),(30.549429,103.950609)]]
    # (30.563688,103.940061),(30.519631,103.936683)
    # (30.563688,103.936922),(30.519631,103.933544)
    # Point = [(30.563688,103.936922),(30.519631,103.933544)]
    # x1 = abs(Point[0][0] - Map._leftMost) * cos(Point[0][0]) * 6371000
    # print('Map:',Map._length,Map.height,Map.width)
    qlearningTest()
