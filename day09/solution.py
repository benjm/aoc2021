import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.readlines()

toid = lambda x,y: str(x)+" "+str(y)

print("starting part1")
h=len(lines)
w=len(lines[0])-1
t=0
lows=[]
for x in range(w):
    for y in range(h):
        c = int(lines[y][x])
        n = []
        if x>0:n.append(lines[y][x-1])
        if x<(w-1):n.append(lines[y][x+1])
        if y>0:n.append(lines[y-1][x])
        if y<(h-1):n.append(lines[y+1][x])
        toadd=c+1
        for m in n:
            if int(m) <= c:
                toadd=0
        t+=toadd
        if toadd > 0:
            xy = toid(x,y)
            lows.append(xy)
print(t)

print("starting part2")
def check(x,y,edg,bas):
    #print(x,y,edg,bas)
    if x<0 or x>=w or y<0 or y>=h: return
    if int(lines[y][x]) > 8: return
    eid = toid(x,y)
    if eid in bas: return
    bas.add(eid)
    edg.add(eid)
    #print("added " + eid)
basins=[]
for low in lows:
    x,y=map(int,low.split())
    basin=set()
    edges=set()
    basin.add(low)
    edges.add(low)
    #print(edges)
    while len(edges) > 0:
        newedges=set()
        for edge in edges:
            ex,ey=map(int,edge.split())
            check(ex-1,ey,newedges,basin)
            check(ex+1,ey,newedges,basin)
            check(ex,ey-1,newedges,basin)
            check(ex,ey+1,newedges,basin)
        #print("check",edges,newedges)
        edges = newedges
    basins.append(len(basin))

big3 = sorted(basins)[-3:]
print(big3, "product = ", big3[0]*big3[1]*big3[2])