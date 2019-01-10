class Actions:
    """
    A collection of static methods for manipulating move actions.
    """
    ### possible action [speed_action,altitude_aciton,heading_action,speed , altitude , heading]#####################################
    
    headinglist = [0,45,90,135,180,225,270,315]

    groundspeedlist = [[0,-10 , 10 ], [0,-5,5,-2,2]]  #m/s    when collision will happen speed -+ 10  

    altitudelist = [[0,-200,200],[0,-100, 100]]   #decline rate at approach stage : 1000ft/min = 5.08m/s ; 20s*5=100 ;
    #when collision will happen altitude -+200 
    # TOLERANCE = .001

    def  change_z(z):
        if z >= 5000:
            z = 5500
        elif z < 5000 and z >= 4000:
            z = 4500
        elif z < 4000 and z >= 3000:
            z = 3500
        elif z < 3000 and z >= 2000:  #queue layer   
            z = 2500
        elif z < 2000 and z >= 1000:   #take off layer
            z = 1500
        else:
            return "contact tower : the altitude is lower than 1000m"   

    # possible action [speed_action,altitude_aciton,heading_action,speed , altitude , heading]                
    def not_atrunway(groundspeed,heading,x,y,z):  # once airplane at the takeoff point the work will transfer to tower 
        if (x == 30.5637 and y ==103.9401 and z =  1500 ) or (x == 30.5196 and y ==103.9367 and z =  1500 ):
            # takeoff_speed = 200*0.5144 = 102.88   ; take off speed 160-200 knot , 1 knot = 1 nmi/h = 0.5144 m/s
            if heading >180 :
                north = 360
            else:
                north = 0
            return [102.88-groundspeed , 1500-z , north- heading, 102.88 , 1500 , 0 ]  
        else:
            return true    

 

    def getPossibleActions( plane , otherplanes):  #collisionplane the plane may crush with me  ; x  the plane need do action 
        heading = plane.heading                                #meetpoint is the point they may collision
        groundspeed = plane.groundspeed * 0.5144   #nmi to m  
        z = Actions.change_z(plane.altitude * 0.3048)   #ft to m
        x = plane.latitude
        y = plane. longitude

        if Actions.not_atrunway(groundspeed,heading,x,y,z) :
            for i in otherplanes:
                other_heading = i.heading
                other_groundspeed = i.groundspeed *0.5144   #nmi/h  to m/s
                other_z = Actions.change_z(i.altitude * 0.3048 ) #ft to m
                other_x = i.latitude
                other_y = i. longitude

                possibleactions= []   

                if (x==other_x and y==other_y and z== other_z): #collision will happen 
                    for a_speed in groundspeedlist[0]: #0,-10 10
                        for a_altitude in altitudelist[0] :# 0,-200, 200
                            for a_heading in headinglist:
                                if a_heading==0 and heading>180
                                    heading_action=360-heading
                                else:
                                    heading_action = a_heading -heading
                                
                                possibleactions.append([a_speed,a_altitude,heading_action,groundspeed+a_speed,z+a_altitude,a_heading])            
                    # alldirection=[]
                    # for i in headinglist:
                    #     alldirection.append([0,0,i-heading,groundspeed,z,i])

                    # possibleactions.append([10,0,0,groundspeed+10,z,heading],[-10,0,0,groundspeed-10,z,heading],
                    #     [0,200,0,groundspeed,z+200,heading],[0,-200,0,groundspeed,z-200,heading])
                    # possibleactions+=alldirection

                    # return(possibleactions)


                 else:
                    for a_speed in groundspeedlist[1]:#0 -5 +5 -2 , +2
                        for a_altitude in altitudelist[1] :# 0,-100, 100
                            for a_heading in headinglist:
                                if a_heading==0 and heading>180
                                    heading_action=360-heading
                                else:
                                    heading_action = a_heading -heading
                                
                                possibleactions.append([a_speed,a_altitude,heading_action,groundspeed+a_speed,z+a_altitude,a_heading])
                return possibleactions               




def next_loaction (airplane,action):
                                  
    v0 = plane.groundspeed * 0.5144   #nmi to m   
    x = airplane.x
    y = airplane.y

    vt = action[3]
    v = (v0+vt)/2
    s=v*20
    s_root2=s/1.41421
    changed_heading =  action[5] 
    if  changed_heading == 0 :
        y += s

    elif changed_heading == 45:
        x += s_root2
        y += s_root2

    elif changed_heading == 90:
        x += s

    elif changed_heading ==135:
        x += s_root2
        y -= s_root2

    elif changed_heading == 180:
        y -= s

    elif  changed_heading == 225:
        x -= s_root2
        y -= s_root2

    elif changed_heading==270:
        x -= s

    elif changed_heading ==315 :
        x -= s_root2
        y += s_root2    


    dict_plane={}
    dict_plane["grounspeed"] = vt
    dict_plane["altitude"] = action[4]
    dict_plane["x"] = x
    dict_plane["y"] = y
    dict_plane["heading"] = changed_heading
    dict_plane["latitude"] = x/55000
    dict_plane["longitude"] = y/5500
    

                    




