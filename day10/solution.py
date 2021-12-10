import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

print("starting part1 & part2 (test expects 26397 and 288957)")

points = {")": 3, "]": 57, "}": 1197, ">": 25137}
compl_points = {")": 1, "]": 2, "}": 3, ">": 4}
pairs = {"(":")","{":"}","[":"]","<":">"}
rev = {")":"(","}":"{","]":"[",">":"<"}
score=0
compl=[]
for line in lines:
    o=""
    #linecopy=""
    noerror=1
    for c in line:
        if noerror:
            if c in "({[<":
                o=o+c
            elif len(o) > 0 and rev[c] == o[-1]:
                o=o[:len(o)-1]
            else:
                score+=points[c]
                noerror=0
                #print(linecopy,c,points[c])
            #linecopy+=c
    if noerror and len(o) > 0:
        temp = 0
        for c in o[::-1]:
            temp = temp * 5 + compl_points[pairs[c]]
        compl.append(temp)
mid = sorted(compl)[len(compl)//2]
print("(1) error score",score)
print("(2) middle completion score",mid)