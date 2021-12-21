import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

print("starting part1")

def updatepos(p,movesize):
    p+=movesize
    if p>10:
        p=p%10
    if p==0:
        p=10
    return p

p1=int(lines[0].split("position: ")[1])
p2=int(lines[1].split("position: ")[1])
nextthrow,maxthrow,perturn,rollcount=1,100,3,0
score1,score2,target=0,0,1000
p1Turn=1
while score1 < target and score2 < target:
    movesize = nextthrow*3 + 3
    nextthrow+=3
    rollcount+=3
    if p1Turn:
        p1=updatepos(p1,movesize)
        score1+=p1
    else:
        p2=updatepos(p2,movesize)
        score2+=p2
    p1Turn = 1 - p1Turn

print(score1,score2,rollcount,rollcount*min(score1,score2))

print("part2: DIRAC DICE")
p1=int(lines[0].split("position: ")[1]) # 4 ... 10
p2=int(lines[1].split("position: ")[1]) # 8 ...  6
# three rolls:
pathsperturn=27 # possible combinations each triple roll, hence number of universes per path on each turn
trios =[3,4,5,6,7,8,9] # seven possible total values from three rolls
ncomb =[1,3,6,7,6,3,1] # number of combinations that reach each possible total. i.e. probability [n out of 27]
mappings={}
for i in range(1,11):
    mappings[i] = list(map(lambda n:[n,n%10][n>10],range(i+3,i+10))) # given starting position i/key, the seven possible spaces the player could move to


sep = ","
def encodePosScore (pos,score):
    return str(pos) + sep + str(score)
def decodePosScore (code):
    return list(map(int,code.split(sep)))

def getTurnWincount(p):
    positionscorecount={} # key "pos,score" value count(==number of universes)
    initialscores = mappings[p]
    for i in range(7):
        position = initialscores[i]
        score = position
        key = encodePosScore(position,score)
        positionscorecount[key] = positionscorecount.get(key,0) + ncomb[i]
    turn = 1
    turnWinCount={}
    turnLiveCount={}
    while sum(positionscorecount.values()) > 0:
        turn+=1
        newPositionScoreCount = {}
        for posScore in positionscorecount.keys():
            startPosition,startScore = decodePosScore(posScore)
            count = positionscorecount[posScore]
            newPositions=mappings[startPosition]
            for i in range(7):
                newPos = newPositions[i]
                newScore = startScore+newPos
                newCount = count*ncomb[i]
                if newScore >= 21:
                    turnWinCount[turn] = turnWinCount.get(turn,0) + newCount
                else:
                    newPosScore = encodePosScore(newPos, newScore)
                    newPositionScoreCount[newPosScore] = newPositionScoreCount.get(newPosScore,0) + newCount
        positionscorecount = newPositionScoreCount
        turnLiveCount[turn] = sum(positionscorecount.values())
    return [turnWinCount,turnLiveCount]

turnWinCountP1,turnLiveCountP1 = getTurnWincount(p1)
turnWinCountP2,turnLiveCountP2 = getTurnWincount(p2)
turns = set()
turns.update(turnWinCountP1.keys())
turns.update(turnWinCountP2.keys())
turns.update(turnLiveCountP1.keys())
turns.update(turnLiveCountP2.keys())
turns = list(sorted(turns))
for turn in turns:
    if turn not in turnWinCountP1:
        turnWinCountP1[turn]=0
    if turn not in turnWinCountP2:
        turnWinCountP2[turn]=0
    if turn not in turnLiveCountP1:
        turnLiveCountP1[turn]=0
    if turn not in turnLiveCountP2:
        turnLiveCountP2[turn]=0

winCount1,winCount2=0,0
for i in range(1,len(turns)):
    turn = turns[i]
    w1 = turnWinCountP1[turn] * turnLiveCountP2[turn-1]
    winCount1+=w1
    w2 = turnWinCountP2[turn] * turnLiveCountP1[turn]
    winCount2+=w2
print(winCount1, winCount2,["P2 Wins","P1 Wins"][winCount1>winCount2])

# given starting value of n this givens 27 possible paths:
# n+[trios]
# e.g. test example first move 4 --> [7,8,9,10,1,2,3] versus 8 --> [1,2,3,4,5,6,7]
# e.g. test exmaple result: player 1 wins in 444356092776315 universes, while player 2 merely wins in 341960390180808 universes.
# 444356092776315
# 341960390180808




