import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.readlines()

print("starting part1")
x = y = 0
for line in lines:
    direction, distance_s = line.split()
    distance = int(distance_s)
    if direction == "forward":
        x += distance
    elif direction == "down":
        y += distance
    else:
        y -= distance
print("part1", x, y, x*y)

print("starting part2")
x = y = aim = 0
for line in lines:
    direction, distance_s = line.split()
    distance = int(distance_s)
    if direction == "forward":
        x += distance
        y += distance * aim
    elif direction == "down":
        aim += distance
    else:
        aim -= distance
    #print(line,x,y,aim)
print("part2 result", x, y, aim, x*y)