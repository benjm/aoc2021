import sys
import math
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

print("starting part1")

lbkt="["
rbkt="]"
sep=","

def split(value):
    didSplit = False
    n=""
    i = 0
    o = ""
    while i < len(value):
        c = value[i]
        if c.isdigit():
            n+=c
        elif len(n) > 0:
            if int(n) > 9:
                nl = str(int(math.floor(float(n)/2)))
                nr = str(int(math.ceil(float(n)/2)))
                splt = lbkt+nl+sep+nr+rbkt
                o+=splt
                o+=value[i:]
                didSplit = True
                i = len(value)
            else:
                o+=n+c
                n=""
        else:
            o+=c
        i+=1
    # if didSplit:
    #     print("SPLIT " + n + " RESULTING IN " + o)
    return [didSplit, o]

def getlr(value,i):
    lr=[]
    n=""
    j = i
    while len(lr)<2:
        c = value[j]
        if c.isdigit():
            n+=c
        elif len(n) > 0:
            lr.append(int(n))
            n=""
        j+=1
    lr.append(j-i)
    return lr

def addleft(value,ln):
    o=""
    i = 1
    n=""
    while i <= len(value):
        c = value[-i]
        if c.isdigit():
            n=c+n
        elif len(n) > 0:
            o=str(int(n)+ln) + o
            o=value[:-i] + c + o
            i=len(value)
        else:
            o=c + o
        i+=1
    return o

def addright(value,rn):
    o=""
    i = 0
    n=""
    while i < len(value):
        c = value[i]
        if c.isdigit():
            n+=c
        elif len(n) > 0:
            o+=str(int(n)+rn)
            o+=value[i:]
            i=len(value)
        else:
            o+=c
        i+=1
    return o

def explode(value, recur=0):
    count = 0
    explodes = False
    i = 0
    imax = len(value)
    o=""
    if (recur > 500):
        print("EXPLODE RECUR LIMIT HIT! "*10,value)
        return value
    while i < imax and not explodes:
        c = value[i]
        if c == lbkt:
            count+=1
        elif c == rbkt:
            count-=1
        if count>4:
            ln,rn,sz = getlr(value,i)
            ls = addleft(value[:i],ln)
            rs = addright(value[i+sz:],rn)
            o=ls+str(0)+rs
            #print("EXPLODING: " + value + " INTO " + o)
            explodes = True
        i+=1
    if explodes:
        return explode(o, recur+1)
    return value

def process(value):
    #print("processing " + value)
    check = True
    while check:
        value = explode(value)
        check, value = split(value)
    return value

def getlrval(value):
    n=0
    lastbutone = len(value)-1
    for i in range(1,lastbutone):
        c = value[i]
        if c == lbkt:
            n+=1
        elif c == rbkt:
            n-=1
        elif c == sep and n == 0:
            l = value[1:i]
            r = value[i+1:lastbutone]
            return [l,r]
    print("ERROR GETTING LR! "*10)


def magnitude(value):
    # 3 * left + 2 * right
    if value.isdigit():
        return int(value)
    l,r=getlrval(value)
    return 3 * magnitude(l) + 2 * magnitude(r)

combine = lambda l,r: lbkt+l+sep+r+rbkt

total=lines[0]
for line in lines[1:]:
    unprocessed = combine(total,line)
    total = process(unprocessed)


print("RESULT:", total)
print("MAGNITUDE:", magnitude(total)) # 3486 for input

print("starting part2")
largest = 0
for i in range(len(lines)):
    for j in range(len(lines)):
        if i != j:
            sz = magnitude(process(combine(lines[i],lines[j])))
            if sz > largest:
                largest = sz
print("LARGEST PAIR: ", largest)