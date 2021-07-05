from itertools import combinations
import time,random

class Card():
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        #Numbered Card
        if rank <= 10:
            self.value = rank
        #Face Card
        elif rank > 10 or rank <=13:
            self.value = 10
        #Ace
        else:
            self.value = 1
    
    def getCard(self):
        return((self.rank,self.suit))

    def showCard(self):
        show = self.rank
        if self.rank == 11:
            show = 'J'
        elif self.rank == 12:
            show = 'Q'
        elif self.rank == 13:
            show = 'K'
        elif self.rank == 14:
            show = 'A'
        return((show,self.suit))

        
class Deck():
    suits = ['D','H','C','S']
    # 11 - J ; 12 - Q ; 13 - K; 14 - A
    vals = [2,3,4,5,6,7,8,9,10,11,12,13,14]
    decklist = []
    def __init__(self):
        self.decklist = []
        for s in self.suits:
            for v in self.vals:
                self.decklist.append(Card(s,v))

    def seeDeck(self):
        deck = []
        for card in self.decklist:
            deck.append(card.getCard())
        return(deck)

    def shuffle(self):
        random.shuffle(self.decklist)

    def drawCard(self):
        return self.decklist.pop(0)


class Player():    
    def __init__(self,name,type):
        self.type = type
        self.name = name
        self.hand = []
        self.played = []
        self.melds = []

    def showHand(self):
        return [x.showCard() for x in self.hand]
    
    def showMelds(self):
        print("Melds in Hand for", self.name,":")
        for meld in self.melds:
            print([y.showCard() for y in meld])
        return

    #Work on this?
    def discard(self,card):
        self.hand.remove(card)
        return(card)

    def calculateHand(self):
        temp_melds = []
        for meld in self.melds:
            temp_melds += [j for j in meld]
        score = 0
        for c in self.hand:
            if c in temp_melds:
                score += 0
            else:
                score += c.value
        return score

    '''
    This checks for melds at the start of a player's turn. Makes sure that the cards in hand and the meld
    pile are in the right.
    '''
    def checkMelds(self):
        ### Copy hand for meld check
        newMelds = self.hand.copy()

        #For cards in melds, remove them from the calculations
        for s in self.melds:
            for c in s:
                try:
                    newMelds.remove(c)
                except:
                    pass


        ## Try to append card to existing melds
        for c in newMelds:
            c_val = c.getCard()[0]
            c_suit = c.getCard()[1]
            set_meld = True
            run_meld = True
            for meld in self.melds:
                #Find if another set, get all vals
                meld_vals = [v.getCard()[0] for v in meld]
                #If the value of cards in meld are not all equal to the card, then it is not a set
                for mv in meld_vals:
                    if mv != c_val:
                        set_meld = False
                if set_meld and len(meld_vals) != 0:
                    meld.append(c)
                    newMelds.remove(c)
                    run_meld = False


                #Check for the Run
                meld_suits = [v.getCard()[1] for v in meld]
                for suits in meld_suits:
                    if suits != c_suit:
                        run_meld = False

                #Check if any of the differences between values is less than 1; non-incremental
                if run_meld:
                    meld_vals.append(c_val)
                    meld_vals.sort()
                    for i in range(1,len(meld_vals)):
                        if meld_vals[i] - meld_vals[i-1] != 1:
                            run_meld = False

                if run_meld:
                    meld.append(c)
                    try:
                        newMelds.remove(c)
                    except:
                        pass

        #All combinations of all possible melds with the remaining cards
        pms = list(combinations(newMelds,3))
        for meld in pms:
            c0 = meld[0].getCard()
            c1 = meld[1].getCard()
            c2 = meld[2].getCard()

            #Check if they are a set; breaks if found after running with new meld
            if c0[0] == c1[0] and c1[0] == c2[0]:
                self.melds.append([meld[0],meld[1],meld[2]])
                self.checkMelds()
                break
            
            #Check if all three cards are in the same suit, break if found after running with new meld
            if c0[1] == c1[1] and c1[1] == c2[1]:
                checkasc = [c0[0],c1[0],c2[0]]
                checkasc.sort()
                if checkasc[2] - checkasc[1] == 1 and checkasc[1] - checkasc[0] == 1:
                    if [meld[0],meld[1],meld[2]] not in self.melds:
                        self.melds.append([meld[0],meld[1],meld[2]])
                        self.checkMelds()
                        break
        return

    '''
    Implement the draw/discard minimax evalaution function here. 
    disc_p : discard pile
    deck : deck

    returns : which pile to choose from adn which card to discard.

    '''

    def myopicMeldScore(self,roots,affixes,deckl):

        type = 0
        try:
            type = len(affixes)
        except:
            type = 2

        #DISCARD PILE CHOICE
        if type == 1:
            #Generate sets of remaining roots where the affix has been replaced.
            possible_hands = {}

            #Iterate over cards, creating all possible meld sets
            for r1 in roots:
                #Replace card with the affixed card
                new_hand = []
                for r2 in roots:
                    if r1 == r2:
                        pass
                    else:
                        new_hand.append(r2)
                new_hand.append(affixes[0])
                possible_hands[r1] = new_hand
            
            disc_vals = {}

            rm = 0

            #Generate rm for each of the hands. This will give us the minimum score
            for k,v in possible_hands.items():

                #See which discard we would pick.
                possible_hand = [c for c in v]

                num_poss_melds = 0
                #Generate combinations of three and check if they are 
                pms = list(combinations(possible_hand,3))

                for meld in pms:
                    c0 = meld[0].getCard()
                    c1 = meld[1].getCard()
                    c2 = meld[2].getCard()

                    if c0[0] == c1[0] and c1[0] == c2[0]:
                        num_poss_melds += 1

                    elif c0[1] == c1[1] and c1[1] == c2[1]:
                        checkasc = [c0[0],c1[0],c2[0]]
                        checkasc.sort()
                        if checkasc[2] - checkasc[1] == 1 and checkasc[1] - checkasc[0] == 1:
                            #print("Found a run!")
                            num_poss_melds += 1         
                
                rm = (num_poss_melds / deckl) * k.value
                disc_vals[k] = rm

            try:
                bestcardtodisc = max(disc_vals,key=disc_vals.get)
                value = disc_vals.get(bestcardtodisc)
            except:
                bestcardtodisc = affixes[0]
                value = rm

            #Returns the card that we would discard and the value of rm that would be used in the evaluation function
            return bestcardtodisc , value

        else:
            #print("Working on the Draw Pile")

            #For every card in the deck, add it to the hand, generate the "rm" value, then add them to a sum. Divide by the total number of cards left in the deck getting an
            #average rm value for choosing to touch the deck

            rm_values = []

            for a in affixes.decklist:
                card, minvalue = self.myopicMeldScore(roots,[a],deckl)
                #print("We found that card:", card.showCard(), " could have a value: ", minvalue)
                rm_values.append(rs - minvalue)

            rmf = sum(rm_values)/len(rm_values)

        return card, rmf

    def chooseDiscard(self,disc_p,deck,hs):
        #Looking to find the minimum values of these
        disc_pile_card = Card('S',5)
        deck_pile_card = Card('S',5)
        disc_pile_min_score = 0
        deck_min_score = 0

        #Ignore cards already in melds
        newMelds = self.hand.copy()
        for s in self.melds:
            for c in s:
                try:
                    newMelds.remove(c)
                except:
                    pass

        #For random actor just pick randomly which card to pick up and a random card to discard.

        if self.type == "R":
            pile_choice = random.randint(1,2)
            disc_pile_card = newMelds[random.randint(0,len(newMelds)-1)]
            return disc_pile_card, pile_choice

        else:
            #Discard Pile Score Calc
            if len(disc_p) == 1:
                disc_pile_card , disc_pile_min_score = self.myopicMeldScore(newMelds,[disc_p[0]],len(deck.decklist))
            else:
                disc_pile_card , disc_pile_min_score = self.myopicMeldScore(newMelds,[disc_p[-1]],len(deck.decklist))

            disc_pile_min_score = hs - disc_pile_min_score

            #print(disc_pile_card.showCard()," is the card we would discard from discard pile. It's evaluation value is: ", disc_pile_min_score)

            #Deck Pile Score Calc

            deck_pile_card, deck_min_score = self.myopicMeldScore(newMelds,deck,len(deck.decklist))


            #print("DISCARD VALUE: ", disc_pile_min_score, " --- DRAW VALUE: ", deck_min_score)

            #print("Current Hand: ",self.showHand())
            #print("Discard Card: ", disc_pile_card.showCard())


            #Draw from Discard Pile if the discard pile minimum is smaller 
            if disc_pile_min_score < deck_min_score:
                return disc_pile_card, 1
            #
            else:
                return deck_pile_card, 2


class Field():
    discardpile = []
    def __init__(self,ps,deck):
        self.deck = deck
        self.deck.shuffle()
        self.players = ps

    def initialDeal(self):
        #Deal 10 cards to each player --------------------- EDIT
        for i in range(10):
            for p in self.players:
                p.hand.append(self.deck.drawCard())
        self.discardpile.append(self.deck.drawCard())


    def showDiscardPile(self):
        return [x.getCard() for x in self.discardpile]

    def drawCard(self):
        return self.discardpile.pop(0)

'''


MAIN #################################################################################################################################################################################################

'''
'''
hi = set of cards in agent's hand
ho = set of KNOWN cards in opponent's hand
D = set of cards in discard pile
t = face-up card on discard pile
Di = the set of cards the agent has discarded
U = set of cards in deck

'''



human_games_won = 0
robot_games_won = 0
human_combacks = 0
robot_comebacks = 0

num_games = 100

times = []

for i in range(num_games):

    print("Game #",i)

    #Main
    robot = Player("Robot","N")

    #Random Actor
    human = Player("Human","R")

    #Normal Actor
    #human = Player("Human","N")
    players = [robot,human]
    ndeck = Deck()
    p_field = Field(players,ndeck)
    p_field.initialDeal()


    last_round = False

    for i in range(100):

        t1 = time.time()

        if len(p_field.deck.decklist) == 1:
            p_field.deck.decklist += p_field.discardpile
            random.shuffle(p_field.deck.decklist)
            p_field.discardpile = [] 
            p_field.discardpile.append(p_field.deck.drawCard())

        robot.checkMelds()

        if len(p_field.deck.decklist) == 1:
            p_field.deck.decklist += p_field.discardpile
            random.shuffle(p_field.deck.decklist)
            p_field.discardpile = [] 
            p_field.discardpile.append(p_field.deck.drawCard())

        human.checkMelds()

        #robot.showMelds()
        #human.showMelds()

        rs = robot.calculateHand()
        hs = human.calculateHand()

        #print("Human Score:", hs)
        #print("Robot Score: ", rs)


        if hs <= 10:
            #Robot last turn
            #print("no h turn")
            score = rs
            p = robot
            last_round = True
        elif rs == 0:
            #print("no r turn")
            score = hs
            p = human
            last_round = True
        
        if last_round:

            if len(p_field.deck.decklist) == 1:
                p_field.deck.decklist += p_field.discardpile
                random.shuffle(p_field.deck.decklist)
                p_field.discardpile = [] 
                p_field.discardpile.append(p_field.deck.drawCard())



            discard_card, pileaction = p.chooseDiscard(p_field.discardpile,p_field.deck,score)

            #print("ROBOT HAND:", p.showHand())
            #print("SHOULD DISCARD?: ", discard_card.showCard())
            #print("BUT HE SHOULD DRAW FROM PILE:", pileaction)
            #print("THIS WAS THE CARD ON THE DISCARD PILE:", p_field.discardpile[0].showCard())

            #Draw from Discard
            if pileaction == 1:
                p.hand.append(p_field.drawCard())
                p_field.discardpile.append(p.discard(discard_card))
            else:
                drawn_c = p_field.deck.drawCard()

                if len(p_field.deck.decklist) == 1:
                    p_field.deck.decklist += p_field.discardpile
                    random.shuffle(p_field.deck.decklist)
                    p_field.discardpile = [] 
                    p_field.discardpile.append(p_field.deck.drawCard())


                #Ignore cards already in melds
                newMelds = p.hand.copy()
                for s in p.melds:
                    for c in s:
                        try:
                            newMelds.remove(c)
                        except:
                            pass

                discard_card, score = p.myopicMeldScore(newMelds,[drawn_c],len(p_field.deck.decklist))
                p.hand.append(drawn_c)

                #print("JUST DREW:", p.showHand())

                #print("FROM DECK DISCARD:",discard_card.showCard())

                p_field.discardpile.append(p.discard(discard_card))

            #print("THIS SHOULD END")
            #print("THERE WERE ", i , " ROUNDS")
            
            break

        for p in players:


            if p == human:
                score = hs
            else:
                score = rs

            #Player Turn - Returns card to discard if discard pile card is draw and the evaluation of the discard card
            discard_card, pileaction = p.chooseDiscard(p_field.discardpile,p_field.deck,score)

            #Draw from Discard
            if pileaction == 1:
                p.hand.append(p_field.drawCard())
                p_field.discardpile.append(p.discard(discard_card))
            else:
                drawn_c = p_field.deck.drawCard()

                if len(p_field.deck.decklist) == 1:
                    p_field.deck.decklist += p_field.discardpile
                    random.shuffle(p_field.deck.decklist)
                    p_field.discardpile = [] 
                    p_field.discardpile.append(p_field.deck.drawCard())

                #Ignore cards already in melds
                newMelds = p.hand.copy()
                for s in p.melds:
                    for c in s:
                        try:
                            newMelds.remove(c)
                        except:
                            pass

                discard_card, score = p.myopicMeldScore(newMelds,[drawn_c],len(p_field.deck.decklist))
                p.hand.append(drawn_c)

                #print("JUST DREW:", p.showHand())

                #print("FROM DECK DISCARD:",discard_card.showCard())

                p_field.discardpile.append(p.discard(discard_card))

            #print(p.showHand())

        #print(i, " round have passed")

        
    #print("Final Scores")

    robot.checkMelds()
    human.checkMelds()

    #robot.showMelds()
    #human.showMelds()

    #print("Final Robot Hand")
    #print(robot.showHand())

    #print("Final Human Hand")
    #print(human.showHand())

    rs = robot.calculateHand()
    hs = human.calculateHand()

    #print("Robot SCore: ", rs)
    #print("Human SCore: ",hs)

    oldrs = rs
    oldhs = hs

    #Check for layoffs at the end of the game

    if rs < hs:
        #print("ROBOT WON: CHECKING IF HUMAN CAN LOWER SCORE")
        #Check if you can add any deadwood cards to the melds of the 'human' player

        #Ignore cards already in melds
        newMelds = human.hand.copy()
        for s in human.melds:
            for c in s:
                try:
                    newMelds.remove(c)
                except:
                    pass

        for c in newMelds:
            #print("Does this card tack on?", c.showCard())
            inSet = True
            inRun = True
            for melds in robot.melds:
                currentmeld_rank = [x.rank for x in melds]
                currentmeld_suit = [x.suit for x in melds]
                #print("Checking this meld:", [x.showCard() for x in melds])

                for r in currentmeld_rank:
                    if c.getCard()[0] != r:
                        inSet = False

                for s in currentmeld_suit:
                    if c.getCard()[1] != s:
                        inRun = False
                
                if inRun:
                    currentmeld_rank.append(c.getCard()[0])
                    #print(currentmeld_rank)
                
                    currentmeld_rank.sort()
                    #print("Sorted: ", currentmeld_rank)

                    for i in range(1,len(currentmeld_rank)):
                        if currentmeld_rank[i] - currentmeld_rank[i-1] != 1:
                            inRun = False

                if inRun or inSet:
                    #print("FOUND CHANGE")
                    hs = hs - c.value
                    break

    else:
        #print("HUMAN WON: CHECKING IF ROBOT CAN LOWER SCORE")
        #Check if you can add any deadwood cards to the melds of the 'human' player

        #For melds in Robot hand check if there is a card in the "H" hand that can tacked on

        #Ignore cards already in melds
        newMelds = robot.hand.copy()
        for s in robot.melds:
            for c in s:
                try:
                    newMelds.remove(c)
                except:
                    pass

        for c in newMelds:
            #print("Does this card tack on?", c.showCard())
            inSet = True
            inRun = True
            for melds in human.melds:
                currentmeld_rank = [x.rank for x in melds]
                currentmeld_suit = [x.suit for x in melds]
                #print("Checking this meld:", [x.showCard() for x in melds])

                for r in currentmeld_rank:
                    if c.getCard()[0] != r:
                        inSet = False

                for s in currentmeld_suit:
                    if c.getCard()[1] != s:
                        inRun = False
                
                if inRun:
                    currentmeld_rank.append(c.getCard()[0])
                    #print(currentmeld_rank)
                
                    currentmeld_rank.sort()
                    #print("Sorted: ", currentmeld_rank)

                    for i in range(1,len(currentmeld_rank)):
                        if currentmeld_rank[i] - currentmeld_rank[i-1] != 1:
                            inRun = False

                if inRun or inSet:
                    #print("FOUND A VALUE!!!!")
                    rs = rs - c.value
                    break


    # print("Old Robot Score: ", oldrs)
    # print("Old Human Score: ", oldhs)


    if hs < rs:
        human_games_won += 1
        if oldhs > oldrs:
            human_combacks +=1
    else:
        robot_games_won +=1
        if oldrs > oldhs:
            robot_comebacks +=1


    #Delete Objects
    del robot
    del human
    del players
    del p_field
    del ndeck

    t2 = time.time()

    times.append(t2-t1)


print("Number of games played: ", num_games)
print("The AI Named 'Human' won ", human_games_won ," games and ", human_combacks ," we won in the comeback round.")
print("The AI Named 'Robot' won ", robot_games_won , "games and ", robot_comebacks, " were won in the comback round")
print("Average Time spent running :", sum(times)/ len(times))
    


