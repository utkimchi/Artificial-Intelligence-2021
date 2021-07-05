#Colton Avila
#CS531
#5/12/21

import pandas as pd, numpy as np, sys
from itertools import combinations

class SudokuPuzzle():
    rc = 9
    start = True

    def __init__(self,board,steps,solved,backtracks,domains,type):
        self.board = board
        self.steps = steps
        self.solved = solved
        self.backtracks = backtracks
        self.domains = domains
        self.type = type

    def getStats(self):
        return[self.steps,self.board,self.backtracks,self.solved]

    def showBoard(self):
        print(self.board)

    #Sets values that need to be checked for square
    def determineSquare(self,row,col):
        rs = []
        cs = []
        if row < 3:
            rs = [0,1,2]
        elif row >= 3 and row < 6:
            rs = [3,4,5]
        elif row >= 6:
            rs = [6,7,8]
        #UL
        if col < 3:
            cs = [0,1,2]
        #UC
        elif col >=3 and col <6:
            cs = [3,4,5]
        #UR
        elif col >= 6:
            cs = [6,7,8]
        return(rs,cs)

    #Check values in row for domain init - Working!
    def setDomains(self,row,col,ic):
        ic = ic
        #Check row values
        for j in range(self.rc):
            if col == j:
                pass
            else:
                cval = self.board.loc[row,j]
                if cval in ic:
                    ic.remove(cval)
        #Check Column values
        for i in range(self.rc):
            if row == i:
                pass
            else:
                rval = self.board.loc[i,col]
                if rval in ic:
                    ic.remove(rval)
        #Check Square!
        sq_rows,sq_cols = self.determineSquare(row,col)
        for r in sq_rows:
            for c in sq_cols:
                if r == row and c == col:
                    pass
                sval = self.board.loc[r,c]
                if sval in ic:
                    ic.remove(sval)
        return(ic)

    def initiateDomains(self):
        for i in range(self.rc):
            rowCon = []
            for j in range(self.rc):
                val = self.board.iloc[i,j]
                if val == 0:
                    #Intial Domains
                    ic = [1,2,3,4,5,6,7,8,9]
                    ic = self.setDomains(i,j,ic)
                    rowCon.append(ic)
                else:
                    rowCon.append([val])
            #calculate domain for every locations [i,j]
            self.domains.append(rowCon)


    def safeSpot(self,rv,cv,val):
        inRow = False
        inCol = False
        inSquare = False
        for i in range(self.rc):
            if i == rv:
                pass
            else:
                if(self.board.loc[i,cv] == val):
                    inRow = True

        for j in range(self.rc):
            if j == cv:
                pass
            else:
                if(self.board.loc[rv,j] == val):
                    inCol = True

        sq_rows,sq_cols = self.determineSquare(rv,cv)
        for r in sq_rows:
            for c in sq_cols:
                if r == rv and c == cv:
                    pass
                else:
                    if(self.board.loc[r,
                    c] == val):
                        inSquare = True
        return(inRow,inCol,inSquare)

    def getNextValues(self,row,col):
        if self.start:
            self.steps = 0
            rv = 0
            cv = 0
            self.start = False
            return(rv,cv)

        elif self.type == "FX":
            rv = 0
            cv = 0
            if col == 8:
                rv = row + 1
                cv = 0
            else:
                rv = row
                cv += col + 1
            return(rv,cv)

        elif self.type == "MC":
            #locations of most contrained
            lowest_set = {}
            for i in range(self.rc):
                for j in range(self.rc):
                    if self.board.loc[i,j] == 0:
                        lowest_set[(i,j)] = len(self.domains[i][j])
            mval = min(lowest_set, key = lowest_set.get)
            return(mval[0],mval[1])

    def emptyDomains(self,row,col,rval):
        #Checks to make sure all domains have at least one value
        is_empty = False
        empty_locs = []
        for j in range(self.rc):
            if col == j:
                pass
            else:
                if rval in self.domains[row][j]:
                    self.domains[row][j].remove(rval)
                    empty_locs.append((row,j,rval))

        for i in range(self.rc):
            if row == i:
                pass
            else:
                if rval in self.domains[i][col]:
                    self.domains[i][col].remove(rval)
                    empty_locs.append((i,col,rval))

        #Check Square!
        sq_rows,sq_cols = self.determineSquare(row,col)
        #print(sq_rows,sq_cols)
        for r in sq_rows:
            for c in sq_cols:
                if r == row and c == col:
                    pass
                elif rval in self.domains[r][c]:
                    self.domains[r][c].remove(rval)
                    empty_locs.append((r,c,rval))

        for f in empty_locs:
            if not self.domains[f[0]][f[1]]:
                is_empty = True

        return empty_locs, is_empty

    #Restore values to domains
    def addDomains(self,elocs):
        for v in elocs:
            self.domains[v[0]][v[1]].append(v[2])

    #RULE 2
    def nakedSingles(self,rv,cv,ds):
        is_empty = False
        locations = []

        #NAKED SINGLE - Remove the the value from any other domain
        
        locations = self.emptyDomains(rv,cv,ds)[0]

        #HIDDEN SINGLE - Look through the domain values of this tile, if there exists a row, column, or square whose cells
        #do not contain the value, then we know this is the only spot and we can remove the values from the other domains

        if len(self.domains[rv][cv]) > 1:
            #Check whole row, take all values, determine if there is a single value. the cell that has that single value can have all of it's other 
            #domains removed
            for i in range(self.rc):
                for vals in self.domains[i][cv]:
                    single = True
                    #check all other domains
                    for x in range(self.rc):
                        if x == i:
                            pass
                        else:
                            if vals in self.domains[x][cv]:
  
                                single = False

                    if single:
                        for rem in self.domains[i][cv]:
                            if vals == rem:
                                pass
                            else:
                                self.domains[i][cv].remove(rem)
                                locations.append((i,cv,rem))

            for j in range(self.rc):
                for vals in self.domains[rv][j]:
                    single = True
                    for y in range(self.rc):
                        if y == j:
                            pass
                        else:
                            if vals in self.domains[rv][y]:
                                single = False
                    
                    if single:
                        for rem in self.domains[rv][j]:
                            if vals == rem:
                                pass
                            else:
                                self.domains[rv][j].remove(rem)
                                locations.append((rv,j,rem))
            

            #Check Square!
            sq_rows,sq_cols = self.determineSquare(rv,cv)
            for r in sq_rows:
                for c in sq_cols:
                    for vals in self.domains[r][c]:
                        single = True
                        for x in sq_rows:
                            for y in sq_rows:
                                if x==r and c==y:
                                    pass
                                else:
                                    if vals in self.domains[x][y]:
                                        single = False
                        if single:
                            #print("Single")
                            for rem in self.domains[r][c]:
                                if vals == rem:
                                    pass
                                else:
                                    #print("Removing ", rem, "from ", self.domains[r][c])
                                    self.domains[r][c].remove(rem)
                                    locations.append((r,c,rem))
        for f in locations:
            if not self.domains[f[0]][f[1]]:
                is_empty = True

        return locations, is_empty

    def nakedPairs(self,rv,cv,ds):
        is_empty = False
        locations = []

        #Check for Naked & Hidden Singles
        locs, isTrue = self.nakedSingles(rv,cv,ds)

        if len(locs) != 0:
            return locs,isTrue

        #NAKED PAIRS
        if len(self.domains[rv][cv]) == 2:

            #Find pair to look for
            base = self.domains[rv][cv]
            base.sort()
            #Row
            for i in range(self.rc):
                if i == rv:
                    pass
                else:
                    #Checks to see if sorted cell domain equal to other cell domain in row
                    #If it is then we go back over the row, skipping the naked pairs, and removing the values
                    rds = self.domains[i][cv]
                    rds.sort()
                    #print("RDS", rds)
                    if rds == base:
                        for k in range(self.rc):
                            #At row for base and row for pair
                            if k == rv or k == i:
                                pass
                            else:
                                for v in base:
                                    if v in self.domains[k][cv]:
                                        self.domains[k][cv].remove(v)
                                        locations.append((k,cv,v))

            for j in range(self.rc):
                if j == cv:
                    pass
                else:
                    cds = self.domains[rv][j]
                    cds.sort()
                    if cds == base:
                        for k in range(self.rc):
                            if k == cv or k == j:
                                pass
                            else:
                                for v in base:
                                    if v in self.domains[rv][k]:
                                        self.domains[rv][k].remove(v)
                                        locations.append((rv,k,v))


            #Check Square!
            sq_rows,sq_cols = self.determineSquare(rv,cv)
            for r in sq_rows:
                for c in sq_cols:
                    if r == rv and c == cv:
                        pass
                    else:
                        sds = self.domains[r][c]
                        sds.sort()
                        if sds == base:
                            for j in sq_rows:
                                for k in sq_cols:
                                    if (r == j and k == c) or (j == rv and k == cv):
                                        pass
                                    else:
                                        for v in base:
                                            if v in self.domains[j][k]:
                                                self.domains[j][k].remove(v)
                                                locations.append((j,k,v))

        #Hidden Pairs
        elif len(self.domains[rv][cv]) > 2:
            combos = combinations(self.domains[rv][cv],2)
            for combo in combos:
                combo = set(combo)
                #Check if hidden pair in row
                for i in range(self.rc):
                    if i == rv:
                        pass
                    else:
                        rd = set(self.domains[i][cv])
                        #If combo subset in cell iteratate back over row removing values if they are equal to any in the combo
                        if combo <= rd:
                            #print("Found Row combo")
                            for cell in range(self.rc):
                                if cell == i or cell == rv:
                                    pass
                                else:
                                    for v in combo:
                                        if v in self.domains[cell][cv]:
                                            self.domains[cell][cv].remove(v)
                                            #X,Y,Value
                                            locations.append((cell,cv,v))
                
                #Check if hidden pair in col
                for j in range(self.rc):
                    if j == cv:
                        pass
                    else:
                        rd = set(self.domains[rv][j])
                        #If combo subset in cell iteratate back over row removing values if they are equal to any in the combo
                        if combo <= rd:
                            #print("Found col combo")
                            for cell in range(self.rc):
                                if cell == j or cell == cv:
                                    pass
                                else:
                                    for v in combo:
                                        if v in self.domains[rv][cell]:
                                            self.domains[rv][cell].remove(v)
                                            #X,Y,Value
                                            locations.append((rv,cell,v))
                #Check Square!
                sq_rows,sq_cols = self.determineSquare(rv,cv)
                for r in sq_rows:
                    for c in sq_cols:
                        if r == rv and c == cv:
                            pass
                        else:
                            rd = set(self.domains[r][c])
                            if combo <= rd:
                                #print("Found square combo")
                                for x in sq_rows:
                                    for y in sq_cols:
                                        if (x == rv and y == cv) or (x==r and y ==c):
                                            pass
                                        else:
                                            for v in combo:
                                                if v in self.domains[x][y]:
                                                    self.domains[x][y].remove(v)
                                                    locations.append((x,y,v))
        # HIDDDDDEN PAIRS
        for f in locations:
            if not self.domains[f[0]][f[1]]:
                is_empty = True
        return locations, is_empty
    
    #Naked triples combo accessor1
    def getCombo(self,rv,cv):
        row_combo = []
        col_combo = []
        square_combo = []
        
        #rows
        for i in range(self.rc):
            for vals in self.domains[i][cv]:
                if vals not in row_combo:
                    row_combo.append(vals)

        for j in range(self.rc):
            for vals in self.domains[cv][j]:
                if vals not in col_combo:
                    col_combo.append(vals)
        
        #Check Square!
        sq_rows,sq_cols = self.determineSquare(rv,cv)
        for r in sq_rows:
            for c in sq_cols:
                for vals in self.domains[r][c]:
                    if vals not in square_combo:
                        square_combo.append(vals)

        rc = combinations(row_combo,3)
        cc = combinations(col_combo,3)
        sc = combinations(square_combo,3)

        return rc,cc,sc


    def nakedTriples(self,rv,cv,ds):
        is_empty = False
        locations = []

        #checks to see if anything was deleted from the earlier constraints, if they are don't move past this
        earlyl,is_empty = self.nakedPairs(rv,cv,ds)

        if earlyl:  
            return earlyl, is_empty
        # NAKED TRIPLEDSSDFS
        else:
            rc,cc,sc = self.getCombo(rv,cv)

            #For each possible comination in the row
            for row_combo in rc:

                row_combo = set(row_combo)
                matches = []

                #Check all values in the row
                for i in range(self.rc):

                    #If cell contains values outside of combo set to false
                    ptrip = True

                    #If cell only has domain of one pass
                    if len(self.domains[i][cv]) <= 1:
                            ptrip = False
                            break

                    #check each value in the domain, if the domain isn't in the combo, pass
                    for v in self.domains[i][cv]:
                        if v not in row_combo:
                            ptrip = False
                            break
                    
                    #If all values in combo, append the cell location
                    if ptrip:
                        matches.append((i,cv))

                
                #If we have three cells with values in the combo -->
                if len(matches) >=3:
                    for i in range(self.rc):
                        if (i,cv) in matches:
                            pass
                        #If the cell is not in the set that represents the combo
                        else:
                            #Get values of the combo
                            for v in row_combo:
                                #If the value is in this non-hang cell
                                if v in self.domains[i][cv]:
                                    #Remove value from domain of thingie 
                                    self.domains[i][cv].remove(v)
                                    locations.append((i,cv,v))

            for column_combo in cc:
                matches = []
                for j in range(self.rc):
                    ptrip = True

                    if len(self.domains[rv][j]) <= 1:
                            ptrip = False
                            break

                    for v in self.domains[rv][j]:
                        if v not in column_combo:
                            ptrip = False
                            break
                    if ptrip:
                        matches.append((rv,j))

                if len(matches) >=3:
                    for j in range(self.rc):
                        if (rv,j) in matches:
                            pass
                        else:
                            for v in column_combo:
                                if v in self.domains[rv][j]:
                                    self.domains[rv][j].remove(v)
                                    locations.append((rv,j,v))

            for square_combo in sc:
                matches = []
                sq_rows,sq_cols = self.determineSquare(rv,cv)
                for r in sq_rows:
                    for c in sq_cols:

                        ptrip = True

                        if len(self.domains[r][c]) <= 1:
                            ptrip = False
                            break

                        for v in self.domains[r][c]:
                            if v not in square_combo:
                                ptrip = False
                                break
                        
                        if ptrip:
                            matches.append((r,c))
                    
                if len(matches) >= 3:
                    for r in sq_rows:
                        for c in sq_cols:
                            if (r,c) in matches:
                                pass
                            else:
                                for v in square_combo:
                                    if v in self.domains[r][c]:
                                        self.domains[r][c].remove(v)
                                        locations.append((r,c,v))

            ############# HIDDEN TRIPLETS
            
            for row_combo in rc:
                combo = set(row_combo)
                matches = []
                #Iterate over row, checking to see if only three cells with more than 2 value contain these values
                for i in range(self.rc):
                    n_domain_vals = combinations(self.domains[i][cv],2)
                    #Iterate over pairs and check to see if the are in the combo
                    for subs in n_domain_vals:
                        subs = set(subs)
                        if subs <= combo:
                            #print("HEy")
                            matches.append([[i],[cv]])

                if len(matches) >= 3:
                    #print("Found matches: ", matches)
                    #print("Combo for matches: ", combo)
                    for i in range(self.rc):
                        if [i,cv] not in matches:
                            for v in combo:
                                if v in self.domains[i][cv]:
                                    self.domains[i][cv].remove(v)
                                    locations.append((i,cv,v))

            for col_combo in cc:
                combo = set(col_combo)
                matches = []

                for j in range(self.rc):
                    n_domain_vals = combinations(self.domains[rv][j],2)
                    for subs in n_domain_vals:
                        subs = set(subs)
                        if subs <= combo:
                            #print("Subs? ", subs)
                            matches.append([[rv],[j]])
                        
                if len(matches) >= 3:
                    for j in range(self.rc):
                        if [rv,j] not in matches:
                            for v in combo:
                                if v in self.domains[rv][j]:
                                    self.domains[rv][j].remove(v)
                                    locations.append((rv,j,v))

            for sq_combo in sc:
                combo = set(sq_combo)
                matches = []
                sq_rows,sq_cols = self.determineSquare(rv,cv)

                for r in sq_rows:
                    for c in sq_cols:
                        n_domain_vals = combinations(self.domains[rv][j],2)
                        for subs in n_domain_vals:
                            subs = set(subs)
                            if subs <= combo:
                                #print("SQUARE SUBS")
                                matches.append([[r],[c]])
                
                if len(matches) >= 3:
                    for r in sq_rows:
                        for c in sq_cols:
                            if [r,c] not in matches:
                                for v in combo:
                                    if v in self.domains[r][c]:
                                        self.domains[r][c].remove(v)
                                        locations.append((r,c,v))

            for f in locations:
                if not self.domains[f[0]][f[1]]:
                    is_empty = True
            return locations, is_empty


    def nakedTriplesSolver(self,rv,cv):
        if 0 not in self.board.values:
            #print("Done")
            self.solved = True
            return(True)

        if self.steps == 1000:
            #print("Did not Complete")
            return(False)
        
        rv,cv = self.getNextValues(rv,cv)
        ogv = self.board.loc[rv,cv]

        #Domains
        for ds in self.domains[rv][cv]:
            self.steps += 1
            if self.steps >= 1000:
                #print("Did not Complete")
                return(False)

            s0,s1,s2 = self.safeSpot(rv,cv,ds)
            if not s0 and not s1 and not s2:
                self.board.loc[rv,cv] = ds
                elocs, empty = self.nakedTriples(rv,cv,ds)

                if not empty:
                    if self.nakedTriplesSolver(rv,cv):
                        return True

                self.addDomains(elocs)
                self.board.loc[rv,cv] = ogv
                self.backtracks += 1
            
        return(False)


    def nakedPairsSolver(self,rv,cv):
        if 0 not in self.board.values:
            #print("Done")
            self.solved = True
            return(True)

        if self.steps == 1000:
            #print("Did not Complete")
            return(False)
        
        rv,cv = self.getNextValues(rv,cv)
        ogv = self.board.loc[rv,cv]

        #Domains
        for ds in self.domains[rv][cv]:
            self.steps += 1
            if self.steps >= 1000:
                print("Did not Complete")
                return(False)

            s0,s1,s2 = self.safeSpot(rv,cv,ds)
            if not s0 and not s1 and not s2:
                self.board.loc[rv,cv] = ds
                elocs, empty = self.nakedPairs(rv,cv,ds)

                if not empty:
                    if self.nakedPairsSolver(rv,cv):
                        return True

                self.addDomains(elocs)
                self.board.loc[rv,cv] = ogv
                self.backtracks += 1
            
        return(False)


    #Hidden Singles
    def nakedSingleSolver(self,rv,cv):

        if 0 not in self.board.values:
            #print("Done")
            self.solved = True
            return(True)

        if self.steps == 1000:
            #print("Did not Complete")
            return(True)

        rv,cv = self.getNextValues(rv,cv)
        ogv = self.board.loc[rv,cv]
        #print("Old value was: ",ogv)

        for ds in self.domains[rv][cv]:
            self.steps += 1
            if self.steps >= 1000:
                #print("Did not Complete")
                return(False)

            s0,s1,s2 = self.safeSpot(rv,cv,ds)
            if not s0 and not s1 and not s2:
                self.board.loc[rv,cv] = ds
                elocs, empty = self.nakedSingles(rv,cv,ds)

                if not empty:
                    if self.nakedSingleSolver(rv,cv):
                        return True

                self.addDomains(elocs)
                self.board.loc[rv,cv] = ogv
                self.backtracks += 1
            
        return(False)


    #NOINFERENCE - Basic Backtracking
    def backtrackingSearch(self,rv,cv):
        if 0 not in self.board.values:
            print("Done")
            self.solved = True
            return(True)

        if self.steps == 1000:
            return(True)
        
        rv,cv = self.getNextValues(rv,cv)
        ogv = self.board.loc[rv,cv]


        for ds in self.domains[rv][cv]:
            
            self.steps += 1
            if self.steps >= 1000:
                #print("Did not Complete")
                return(False)

            s0,s1,s2 = self.safeSpot(rv,cv,ds)

            if not s0 and not s1 and not s2:
                self.board.loc[rv,cv] = ds
                if self.backtrackingSearch(rv,cv):
                    return True
                self.board.loc[rv,cv] = ogv
                self.steps+=1
                self.backtracks += 1
        return(False)

    def solve(self,nn):
        self.initiateDomains()
        #NO INFERENCE
        if nn == "NI":
            self.nakedSingleSolver(0,0)
        elif nn == "FC":
            self.backtrackingSearch(0,0)
        elif nn == "NP":
            self.nakedPairsSolver(0,0)
        elif nn == "TRIP":
            self.nakedTriplesSolver(0,0)
                
    
#Open Sudoku files
with open("C:\\Users\\colto\\Documents\\Oregon\\21S - Artifical Intelligence\\Homeworks\\Sudoku\\sudoku-problems.txt") as f:
    contents = f.readlines()


################## ALL OF THE FILES

## PARSING TEXT FILE
c = 1
d = 10
sudoku_puzzles = []
for i in range (0,77):
    tot_arr = []
    while c < d:
        rv = []
        for v in contents[c]:
            if v not in [" ", "\n","\t"]:
                rv.append(int(v))
        tot_arr.append(rv)
        c += 1
    sudoku_puzzles.append(tot_arr)
    c = d + 2
    d += 11
        

print(len(sudoku_puzzles))

nonzeros = []
solved = []
bks = []
sols = []
steps = []

nonzeros2 = []
solved2 = []
bks2 = []
sols2 = []
steps2 = []


###### MAIN
#######################################################
######################################################
######################################################

'''
    def solve(self,nn):
        self.initiateDomains()
        #NO INFERENCE
        if nn == "NI":
            self.nakedSingleSolver(0,0)
        elif nn == "FC":
            self.backtrackingSearch(0,0)
        elif nn == "NP":
            self.nakedPairsSolver(0,0)
        elif nn == "TRIP":
            self.nakedTriplesSolver(0,0)

    Select the value for nn and place it in the arguments of SudokuPuzzle
    'FX' = Fixed Baseling
    'MC' = Most Constrained Variable

'''



c = 0
for p in sudoku_puzzles:
    lo = []
    c+=1
    input()
    df = pd.DataFrame(p)
    print("PUZZLE #", c)
    nonzeros.append(np.count_nonzero(df))
    print("NONZERO CELLS -->",np.count_nonzero(df))

    print("FIXED BASELINE - NO INFERENCE")
    pz = SudokuPuzzle(df,0,False,0,[],'FX')
    pz.solve("FC")
    stats = pz.getStats()
    steps.append(stats[0])
    sols.append(stats[1])
    bks.append(stats[2])
    solved.append(stats[3])

    pz.showBoard()

    print("Solved?")
    print(stats[3])
    print("Backtracks")
    print(bks)

    print("MCV - NO INFERENCE")
    #FX is other
    pz2 = SudokuPuzzle(df,0,False,0,[],'MC')
    pz2.solve("FC")
    stats2 = pz2.getStats()
    steps2.append(stats2[0])
    sols2.append(stats2[1])
    bks2.append(stats2[2])
    solved2.append(stats2[3])

    pz2.showBoard()

    print("Steps")
    print(steps2)
    print("Backtracks")
    print(bks2)
    print("Solved?")
    print(solved2)

    pz3= SudokuPuzzle(df,0,False,0,[],'FX')
    pz3.solve("NI")
    pz4 = SudokuPuzzle(df,0,False,0,[],'MC')
    pz4.solve("NI")
    pz5 = SudokuPuzzle(df,0,False,0,[],'FX')
    pz5.solve("NP")
    pz6 = SudokuPuzzle(df,0,False,0,[],'MC')
    pz6.solve("NP")
    pz7 = SudokuPuzzle(df,0,False,0,[],'FX')
    pz7.solve("TRIP")
    pz8 = SudokuPuzzle(df,0,False,0,[],'MC')
    pz8.solve("TRIP")

    pz8.showBoard()


    lo.append("NI-FB")
    lo.append(pz.solved)
    lo.append(pz.backtracks)
    lo.append("NI-MCV")
    lo.append(pz2.solved)
    lo.append(pz2.backtracks)
    lo.append("NHS-FB")
    lo.append(pz3.solved)
    lo.append(pz3.backtracks)
    lo.append("NHS-MCV")
    lo.append(pz4.solved)
    lo.append(pz4.backtracks)
    lo.append("NHP-FB")
    lo.append(pz5.solved)
    lo.append(pz5.backtracks)
    lo.append("NHP-MCV")
    lo.append(pz6.solved)
    lo.append(pz6.backtracks)
    lo.append("NHT-FB")
    lo.append(pz7.solved)
    lo.append(pz7.backtracks)
    lo.append("NHT-MCV")
    lo.append(pz8.solved)
    lo.append(pz8.backtracks)

    print(lo)
    lo = []
    



#All of information
print(steps)
print(bks)
print(solved)

print(steps2)
print(bks2)
print(solved)


