import pandas as pd, numpy as np, random, matplotlib.pyplot as plt
from queue import PriorityQueue
import time
class Node:
    heuristic = None
    instances = 0 
    xloc = None
    yloc = None
    moves = []
    fn = None

    def __init__(self,state,parent,action,path_cost,htype):
        self.parent = parent
        self.state = state
        self.action = action
        self.get0()
        if htype == "Manhattan":
            self.ManhattenDistance()
        else:
            self.Misplaced()

        #Checks if parent exists in order to generate g(n)
        if parent:
            self.path_cost = parent.path_cost + path_cost
        else:
            self.path_cost = path_cost

        self.fn = self.path_cost + self.heuristic
        
    def showGame(self):
        print(self.state)

    def goal(self):
        if np.array_equal(self.state,goalb):
            return True
        else:
            return False
    
    def get0(self):
        zpos = np.where(self.state == 0)
        self.xloc = zpos[0]
        self.yloc = zpos[1]
    
    def possibleMoves(self):
        #Determines legal moves
        moves = ['U','D','L','R']
        if self.xloc == 0:
            moves.remove('U')
        elif self.xloc ==3:
            moves.remove('D')
        if self.yloc == 0:
            moves.remove('L')
        elif self.yloc == 3:
            moves.remove('R')
        self.moves = moves
    
    def createDownStream(self, htype):
        children = []
        self.possibleMoves()
        #Each valid movement create a new child node
        for a in self.moves:
            new_state = self.state.copy()
            new_state = Move(new_state,a,self.xloc,self.yloc)
            children.append(Node(new_state,self,a,1,htype))
        return(children)

    def ManhattenDistance(self):
        self.heuristic = 0
        for i in range(0,16):
            cur = np.where(self.state == i)
            goal = np.where(goalb == i)
            dist = abs(goal[0] - cur[0]) + abs(goal[1] - cur[1])
            self.heuristic += dist
    
    def Misplaced(self):
        self.heuristic = 0
        for i in range(0,16):
            cur = np.where(self.state == i)
            goal = np.where(goalb == i)

            if cur != goal:
                self.heuristic += 1 
    
    #Follow parent list and take actions to create steps
    def generateSolution(self):
        solution = []
        solution.append(self.action)
        path = self
        #Until you reach the top node
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]
        solution.reverse()
        #self.showGame()
        return solution
    
############################################################################### Depth Limited Search

def It_Deep_A_Search(j,heur):
    #Required for ID in priority Q
    count=0
    #Priority queue rankes them based on the heuristic "fn"
    q = PriorityQueue()
    q.put((j.fn,count,j))
    #While frontier still has memebers, keep searching
    while not q.empty():
        global nco
        curn = q.get()
        curn = curn[2]
        if curn.goal():
            return curn.generateSolution()
        children = curn.createDownStream(heur)
        for n in children:
            nco +=1
            count+=1
            q.put((n.fn,count,n))


############################################################################## Recursive Best-First Search

def rec_bfs(state,heur):
    node = RBFS(Node(state,None,None,0,heur),maxxx,heur)
    con = node[1]
    node = node[0]
    return node.generateSolution()

def RBFS(j,f_limit,heur):
    global nco
    count = 0 
    successors = []

    if j.goal():
        return j, count
    children = j.createDownStream(heur)

    if not len(children):
        return None, f_limit

    count =-1

    for c in children:
        nco += 1
        count += 1
        c.fn = max(c.fn,j.fn)
        successors.append((c.fn,count,c))
        
    while len(successors):
        successors.sort()
        #Node with lowest f-value
        if successors[0][2].fn > f_limit:
            return None, successors[0][2].fn
        #second lowest f
        alternative = successors[1][0]
        result, successors[0][2].fn = RBFS(successors[0][2],min(f_limit,alternative),heur)
        successors[0] = (successors[0][2].fn,successors[0][1],successors[0][2])
        if result != None:
            break
    return result, None

    
#############################################################################################################


####
#
#  MAIN
####


######### 
# 
# :SCRAMBLE GENERATION
#
########

#get legal moves
def getMove(x,y):
    #Determines legal moves
    moves = ['U','D','L','R']
    if x == 0:
        moves.remove('U')
    elif x ==3:
        moves.remove('D')
    if y == 0:
        moves.remove('L')
    elif y == 3:
        moves.remove('R')
    return(moves[random.randint(0,len(moves)-1)])
#shuffle move the board
def Move(board,direction,x,y):
    if direction == 'U':
        board[x,y] = board[x-1,y]
        board[x-1,y] = 0
    elif direction == 'D':
        board[x,y] = board[x+1,y]
        board[x+1,y] = 0
    elif direction == 'L':
        board[x,y] = board[x,y-1]
        board[x,y-1] = 0
    elif direction == 'R':
        board[x,y] = board[x,y+1]
        board[x,y+1] = 0
    return(board)
#Take a network and shuffle it from the point of the 0
def Scramble(m):
    nboard = goalb.copy()
    for i in range(m):
        zpos = np.where(nboard == 0)
        direction = getMove(zpos[0],zpos[1])
        nboard = Move(nboard,direction,zpos[0],zpos[1])
    return nboard
        
heur = "Misplaced"

#Goal array
goalb = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])

#Maximum Frontier
maxxx = 100000

#times manhattan r
tma = []
#time misplaced r
tmi = []
#time manhattan a
tmaa = []
#time misplaced a
tmia = []

#nodes manhattan r
nma = []
#nodes misplaced r
nmi = []
#nodes manhattan a
nmaa = []
#nodes misplaced a
nmia = []

#length manhattan r
lma = []
#length misplace r
lmi = []
#length manhattan a
lmaa = []
#length misplaced a
lmia = []


#m = [10,20,30,40,50]
m = [40,50]
for steps in m:
    for number in range(0,10):
        #Node counts
        nco = 0


        fresh_board = Scramble(steps)
        #Manhattan - RBFS
        t0 = time.time()
        manrbfs = rec_bfs(fresh_board,"Manhattan")
        t1 = time.time()
        lma.append(len(manrbfs))
        tma.append(t1-t0)
        nma.append(nco)

        #Node counts
        nco = 0

        t0 = time.time()
        misrbfs = rec_bfs(fresh_board,"Misplaced")
        t1 = time.time()
        lmi.append(len(misrbfs))
        tmi.append(t1-t0)
        nmi.append(nco)

        #Node counts
        nco = 0

        #IDA
        n1 = Node(fresh_board,None,None,0,"Manhattan")
        t0 = time.time()
        manida = It_Deep_A_Search(n1,"Manhattan")
        lmaa.append(len(manida))
        t1 = time.time()
        tmaa.append(t1-t0)
        nmaa.append(nco)

        #Node counts
        nco = 0

        n2 = Node(fresh_board,None,None,0,"Misplaced")
        t0 = time.time()
        misida = It_Deep_A_Search(n2,"Misplaced")
        t1 = time.time()
        lmia.append(len(misida))
        tmia.append(t1-t0)
        nmia.append(nco)

ss = 2

#Times
#times manhattan r
tma = np.array_split(tma,ss)
#time misplaced r
tmi = np.array_split(tmi,ss)
#time manhattan a
tmaa = np.array_split(tmaa,ss)
#time misplaced a
tmia = np.array_split(tmia,ss)

print(tma)
print(tmi)
print(tmaa)
print(tmia)

nma = np.array_split(nma,ss)
nmi = np.array_split(nmi,ss)
nmaa = np.array_split(nmaa,ss)
nmia = np.array_split(nmia,ss)

print(nma)
print(nmi)
print(nmaa)
print(nmia)

lma = np.array_split(lma,ss)
lmi = np.array_split(lmi,ss)
lmaa = np.array_split(lmaa,ss)
lmia = np.array_split(lmia,ss)

print(lma)
print(lmi)
print(lmaa)
print(lmia)


for i in range(1,ss+ 1):
    plt.bar(["Manhattan RBFS","Misplaced RBFS","Manhattan IDA*","Misplaced IDA*"],[np.average(tma[i-1]),np.average(tmi[i-1]),np.average(tmaa[i-1]),np.average(tmia[i-1])])
    plt.title("Runtime")
    plt.show()

    print("Average times")
    print([np.average(tma[i-1]),np.average(tmi[i-1]),np.average(tmaa[i-1]),np.average(tmia[i-1])])

for i in range(1,ss + 1):
    plt.bar(["Manhattan RBFS","Misplaced RBFS","Manhattan IDA*","Misplaced IDA*"],[np.average(nma[i-1]),np.average(nmi[i-1]),np.average(nmaa[i-1]),np.average(nmia[i-1])])
    plt.title("Number of Nodes")
    plt.show()

    print("Average Nodes")
    print([np.average(nma[i-1]),np.average(nmi[i-1]),np.average(nmaa[i-1]),np.average(nmia[i-1])])

for i in range(1,ss + 1):
    plt.bar(["Manhattan RBFS","Misplaced RBFS","Manhattan IDA*","Misplaced IDA*"],[np.average(lma[i-1]),np.average(lmi[i-1]),np.average(lmaa[i-1]),np.average(lmia[i-1])])
    plt.title("Length of Optimal Path")
    plt.show()
    
    print("Average Path Lengths")
    print([np.average(lma[i-1]),np.average(lmi[i-1]),np.average(lmaa[i-1]),np.average(lmia[i-1])])