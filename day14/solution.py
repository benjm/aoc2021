import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

print("starting part1")
template = lines[0]
poly = template
pairDict = {}
for line in lines[2:]:
    pair,mid = line.split(" -> ")
    pairDict[pair] = mid

for turn in range(10):
    temp = ""
    for i in range(len(poly)-1):
        pair = poly[i:i+2]
        temp+=poly[i]+pairDict.get(pair,"")
    poly = temp+poly[-1]

count = {}
for c in poly:
    count[c] = count.get(c,0)+1

values = sorted(list(count.values()))

print("part 1 (brute force) done: ",values[-1] - values[0])

print("starting part2")
poly = template
pairmap = {}
for i in range(len(poly)-1):
    pair = poly[i:i+2]
    pairmap[pair] = pairmap.get(pair,0)+1

for turn in range(40):
    temp = {}
    for pair in pairmap.keys():
        mid = pairDict.get(pair,"")
        if len(mid) == 0:
            temp[pair] = temp.get(pair,0)+pairmap[pair]
        else:
            lpair = pair[0] + mid
            rpair = mid + pair[1]
            temp[lpair] = temp.get(lpair,0)+pairmap[pair]
            temp[rpair] = temp.get(rpair,0)+pairmap[pair]
    pairmap = temp

count = {}
for pair in pairmap.keys():
    for c in pair:
        count[c] = count.get(c,0)+pairmap[pair]

actualCount = {}
for c in count.keys():
    actualCount[c] = int(count[c]/2)
    #counting pairs means ever character except the first and last are counted twice
    if c == template[0] or c == template[-1]: actualCount[c]+=1

values = sorted(list(actualCount.values()))

print("part 2 (sneakier) done: ",values[-1] - values[0])






