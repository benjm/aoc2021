import sys
import math
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.readlines()

pos = list(sorted(map(int,lines[0].split(","))))
tot = float('inf')
i = -1
for p in range(pos[0], pos[-1]):
    t = sum(map(lambda x:abs(x - p),pos))
    if t < tot:
        tot = t
        i = p
print("part1:", i, tot) # 342 --> 325528

# mid = (len(pos)+1)/2.0
# x=int(math.ceil(mid))
# leftsum = sum(pos[:x])
# rightsum = sum(pos[x:])
# # mean = 342
# print(pos[x-1:x+1], leftsum, rightsum)


print("starting part2 inefficient version")

def fuelincr(x,p):
    return sum(range(0,abs(x-p)+1))

tot = float('inf')
i = -1
for p in range(pos[0], pos[-1]):
    t = sum(map(lambda x:fuelincr(x,p),pos))
    if t < tot:
        tot = t
        i = p
print("part2:", i, tot) # 460, 85015836