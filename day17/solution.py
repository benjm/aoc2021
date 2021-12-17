import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

print("starting part1")
rangex,rangey=lines[0].split(" x=")[1].split(", y=")
xmin,xmax=map(int,rangex.split(".."))
ymin,ymax=map(int,rangey.split(".."))

print("target:",[xmin,xmax,ymin,ymax])

# find lowest x value(s) that will end on x=0 in the target area (to allow for max y, not constrained by x)
i=1
t=0
lowx=[]
while t < xmax:
    t=sum(range(i+1))
    if xmin<=t<=xmax:
        lowx.append(i)
    i+=1

# y goes (where n is positive) through n,n-1...,1,0,-1...-n at which point it's back on y=0
# assuming x is static by this point y continues through range -(n+1),-(n+2)

besty=abs(ymin)-1

print("x="+str(lowx),"y="+str(besty),"height="+str(sum(range(abs(ymin)))))

print("starting part2")
# find all possible x values
possiblex=list(range(xmax,xmin-1,-1))
lowestx=min(lowx)
checkx=list(range(xmin-1,lowestx-1,-1))
for i in range(len(checkx)):
    fullcheckx=list(range(checkx[i],0,-1))
    d=0
    j=0
    while d < xmax:
        d+=fullcheckx[j]
        if xmax>=d>=xmin:
            possiblex.append(checkx[i])
            d=xmax # end the loop
        j+=1
print("possiblex",possiblex)

# for each possible x value
# find [num steps] when it falls within the target area
# find possible y values for each [num steps] that fall into the target area

distinct=0
possibleymap={}
possibleymap[1] = set(range(ymin,ymax+1))
for x in possiblex:
    nxsteps=[]
    dx=x
    totx=0
    i=0
    while totx<xmax and dx>0:
        totx+=dx
        dx-=1
        i+=1
        if xmin<=totx<=xmax:
            nxsteps.append(i)
    if dx<1 and totx<=xmax:
        # x remains constant so can carry of with n...
        for j in range(i+1,i+1000): #this is HORRIBLE ... but it worked
            nxsteps.append(j)

    possibley=set()
    for n in nxsteps:
        if n not in possibleymap:
            okay=set()
            for y in range(ymin,besty+1):
                if y>=0:
                    above = 2*y+1
                    if above < n:
                        rem = n - above
                        ypos = -(rem*(y+1) + (rem*(rem-1))/2)
                        if ymin<=ypos<=ymax:
                            okay.add(y)
                            #print("CALC x,n,above,y,ypos",x,n,above,y,ypos)
                else:
                    rem = n-1
                    ypos = n*y - (rem*(rem+1))/2
                    if ymin<=ypos<=ymax:
                        okay.add(y)
                        #print("CALC x,n,y,ypos",x,n,y,ypos)
            possibleymap[n] = okay
            #print("-----------------------> calculated possible y for n=",n,"as",okay)
        possibley.update(possibleymap[n])
    distinct+=len(possibley)
    #print("x,[y],distinct",x,possibley,distinct)

print("distinct",distinct)


