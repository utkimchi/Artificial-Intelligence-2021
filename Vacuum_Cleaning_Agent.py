import pandas as pd, numpy as np , random as rnd, matplotlib.pyplot as plt


#Generate empty room
def genroomA():
    #Init df1
    a = np.zeros((12,12))
    #Walls
    a[0,:] = 9
    a[:,0] = 9
    a[:,11] = 9
    a[11,:] = 9
    return(a)
#Generate walled room
def genroomB():
    b = np.zeros((13,13))
    #Walls & Doors
    b[0,:] = 9
    b[:,0] = 9
    b[:,12] = 9
    b[12,:] = 9
    b[:,6] = 9
    b[6,:] = 9
    b[3,6] = 0
    b[6,3] = 0
    b[9,6] = 0
    b[6,9] = 0
    return(b)
#turn right
def turnR(dir):
    if dir == [-1,0]:
        dir = [0,1]
    elif dir == [0,1]:
        dir = [1,0]
    elif dir == [1,0]:
        dir = [0,-1]
    elif dir == [0,1]:
        dir = [-1,0]
    return(dir)
#turn left
def turnL(dir):
    if dir == [-1,0]:
        dir = [0,-1]
    elif dir == [0,1]:
        dir = [-1,0]
    elif dir == [1,0]:
        dir = [0,1]
    elif dir == [0,-1]:
        dir = [1,0]
    return(dir)

#1. Simple Memory-less Deterministic Reflex Agent - 

def runAgent1(is_on,walls,cl):

    numClean = []
    numSteps = []
    home = cl
    #Facing N
    dir = [-1,0]
    df = pd.DataFrame(walls)
    steps = 0

    while is_on:

        #Calculate Next Step in Dir for Wall Sensor
        ncl = tuple(np.array(list(cl)) + np.array(dir))

        #Home Sensor Wall Sensor Dirt Sensor
        if cl == home and df.at[ncl] == 9 and df.at[cl] == 0:
            df.at[cl] = 1

        #Dirt Sensor & Home Sensor Activated
        elif df.at[cl] == 0 and cl == home:
            cl = ncl
            
        #Only Dirt Sensor
        elif df.at[cl] == 0:
            df.at[cl] = 1

        #Home Sensor, Wall Sensor
        elif cl == home and df.at[ncl] == 9:
            is_on = False
            steps -= 1

        #Only Wall Sensor
        elif df.at[ncl] == 9:
            #Update Direction (Turn Right)
            #Facing N
            if dir == [-1,0]:
                dir = [0,1]
            elif dir == [0,1]:
                dir = [1,0]
            elif dir == [1,0]:
                dir = [0,-1]
            elif dir == [0,1]:
                dir = [-1,0]
        #Move foward if no sensors activated
        else:
            cl = ncl

        #Number of steps counter
        steps += 1
        numSteps.append(steps)
        #Number of Clean:

        numClean.append(sum(np.sum(df == 1)))

        if steps >= 1000:
            break
    
    print("End Tile: ", cl)
    print("Number of steps taken: ", steps)
    print("Visualization of Environment --")
    print(df)

    return [numClean,numSteps]

#2. Randomized Reflex agent that can choose actions randomly based on sensor readings
def runAgent2(is_on,walls,cl):

    numClean = []
    numSteps = []

    home = cl
    #Facing N
    dir = [-1,0]
    df = pd.DataFrame(walls)
    steps = 0

    while is_on:

        #Calculate Next Step in Dir for Wall Sensor
        ncl = tuple(np.array(list(cl)) + np.array(dir))

        #Home Sensor Wall Sensor Dirt Sensor
        if cl == home and df.at[ncl] == 9 and df.at[cl] == 0:
            df.at[cl] = 1

        #Dirt Sensor & Home Sensor Activated
        elif df.at[cl] == 0 and cl == home:
            cl = ncl
            
        #Only Dirt Sensor
        elif df.at[cl] == 0:
            df.at[cl] = 1

        #Home Sensor, Wall Sensor
        elif cl == home and df.at[ncl] == 9:
            is_on = False
            steps -= 1

        #Only Wall Sensor
        elif df.at[ncl] == 9:
            #Update Direction (Turn Right)
            p = rnd.random()
            if p <= 0.5:
                dir = turnR(dir)
            else:
                dir = turnL(dir)
        #If no sensors activated choose to turn, or move foward
        else:
            p = rnd.random()
            #25% chance turn left
            if p < .1:
                dir = turnL(dir)
            #25% chance turn right
            elif p > 0.1 and p < 0.5:
                dir = turnR(dir)
            #50% chance go straight
            else:
                cl = ncl
        
        #Number of steps counter
        steps += 1
        numSteps.append(steps)
        #Number of Clean:

        numClean.append(sum(np.sum(df == 1)))

        if steps >= 1000:
            break
        #500,000 steps == Battery Running Out
        if steps >= 500000:
            break
    print("End Tile: ", cl)
    print("Number of steps taken: ", steps)
    print("Visualization of Environment --")
    print(df)

    return [numClean,numSteps]

# 3-Byte Deterministic Reflex Agent

def runAgent3(is_on,walls,cl):

    #For Plotting

    numClean = []
    numSteps = []


    home = cl
    #Facing N
    dir = [-1,0]
    df = pd.DataFrame(walls)
    steps = 0

    #3 bytes of information; Keeps track of a recent turn.
    turned_l = False
    turned_r = True
    #Keeps state that it is turning
    inturn = False

    while is_on:

        #Calculate Next Step in Dir for Wall Sensor
        ncl = tuple(np.array(list(cl)) + np.array(dir))

        #Home Sensor Wall Sensor Dirt Sensor
        if cl == home and df.at[ncl] == 9 and df.at[cl] == 0:
            df.at[cl] = 1

        #Dirt Sensor & Home Sensor Activated
        elif df.at[cl] == 0 and cl == home:
            cl = ncl

        
        #If in turn and dirt sensor detected; turn
        elif turned_r and df.at[cl] == 0 and inturn == True:
            dir = turnR(dir)
            turned_r = False
            turned_l = True
            inturn = False

        elif turned_l and df.at[cl] == 0 and inturn == True:
            dir = turnL(dir)
            turned_l = False
            turned_r = True
            inturn = False
            
        #Only Dirt Sensor
        elif df.at[cl] == 0:
            df.at[cl] = 1

        #Home Sensor, Wall Sensor, and Dirt Censor
        elif cl == home and df.at[ncl] == 9 and df.at[cl] == 1:
            is_on = False
            steps -= 1

        #Only Wall Sensor
        elif df.at[ncl] == 9:
            if turned_l:
                dir = turnL(dir)
            else:
                dir = turnR(dir)
            inturn = True
        else:
            cl = ncl

        #Number of steps counter
        steps += 1
        numSteps.append(steps)
        #Number of Clean:

        numClean.append(sum(np.sum(df == 1)))
        #500,00 steps == Battery Running Out

        if steps >= 500:
            break
        
    print("End Tile: ", cl)
    print("Number of steps taken: ", steps)
    print("Visualization of Environment --")
    print(df)

    return [numClean,numSteps]


#Init df 1
a = genroomA()
#Init df 2
b = genroomB()

print("Simple Memory-Less Deterministic Reflex Agent: Empty Grid")
r1 = runAgent1(True,a,(10,1))
print("Simple Memory-Less Deterministic Reflex Agent: Walls with Door")
r2 = runAgent1(True,b,(11,1))


#LOOP OF RANDOM

random_cleans_e = []
random_steps_e = []

random_cleans_d = []
random_steps_d = []

for i in range(0,51):
    #Init df 1
    a = genroomA()
    #Init df 2
    b = genroomB()

    print("Random Memory-Less Deterministic Reflex Agent: Empty")
    r3 = runAgent2(True,a,(10,1))
    print("Random Memory-Less Deterministic Reflex Agent: Doors")
    r4 = runAgent2(True,b,(11,1))

    random_steps_e.append(r3[1][-1])
    random_cleans_e.append(r3[0][-1])

    random_steps_d.append(r4[1][-1])
    random_cleans_d.append(r4[0][-1])


#Init df 1
a = genroomA()
#Init df 2
b = genroomB()

print("Deterministic Model-Based Reflex Agent w/ State Memory: Empty Room")
r5 = runAgent3(True,a,(10,1))

print("Deterministic Model-Based Reflex Agent w/ State Memory: Walled Room")
r6 = runAgent3(True,b,(11,1))

########################### PLOTTING - Uncomment to see plots ################################################################################

plt.figure(0)
plt.title("Simple Memory-Less Deterministic Reflex Agent: Empty Room")
plt.plot(r1[1],r1[0])
plt.xlabel("Steps")
plt.ylabel("# of Clean Tiles")
plt.show()


plt.figure(1)
plt.title("Simple Memory-Less Deterministic Reflex Agent: Walled Room")
plt.plot(r2[1],r2[0])
plt.xlabel("Steps")
plt.ylabel("# of Clean Tiles")
plt.show()

plt.figure(2)
plt.title("Random Memory-Less Deterministic Reflex Agent: Empty Room - 50 Runs")
plt.scatter(np.array(random_steps_e),np.array(random_cleans_e))
plt.xlabel("Steps")
plt.ylabel("# of Clean Tiles")
plt.show()

plt.figure(3)
plt.title("Random Memory-Less Deterministic Reflex Agent: Walled Room")
plt.scatter(np.array(random_steps_d),np.array(random_cleans_d))
plt.xlabel("Steps")
plt.ylabel("# of Clean Tiles")
plt.show()

plt.figure(4)
plt.title("Memory Deterministic Reflex Agent: Empty Room")
plt.plot(r5[1],r5[0])
plt.xlabel("Steps")
plt.ylabel("# of Clean Tiles")
plt.show()

plt.figure(5)
plt.title("Memory Deterministic Reflex Agent: Walled Room")
plt.plot(r6[1],r6[0])
plt.xlabel("Steps")
plt.ylabel("# of Clean Tiles")
plt.show()



##### SUMMARY STATISTICS #################################################

perfs = []
perfs.append(r1[0][-1]/r1[1][-1])
perfs.append(r2[0][-1]/r2[1][-1])
perfs.append(r5[0][-1]/r5[1][-1])
perfs.append(r6[0][-1]/r6[1][-1])

cleaned = []
cleaned.append(r1[0][-1])
cleaned.append(r2[0][-1])
cleaned.append(r5[0][-1])
cleaned.append(r6[0][-1])

#Performance Metrics
print(perfs)
#Number of tiles Cleaned
print(cleaned)

pe = []
pd = []

ce = []
cd = []

se =[]
sd = []

for i in range(len(random_cleans_e)):
    pe.append(random_cleans_e[i]/random_steps_e[i])
    pd.append(random_cleans_d[i]/random_steps_d[i])
    ce.append(random_cleans_e)
    cd.append(random_cleans_d)
    se.append(random_steps_e)
    sd.append(random_steps_d)


print("performance measures 50r")
print(np.mean(pe))
print(np.mean(pd))

print("cleans 50r")
print(np.mean(ce))
print(np.mean(cd))

print("steps 50r")
print(np.mean(se))
print(np.mean(sd))