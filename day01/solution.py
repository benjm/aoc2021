import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.readlines()

count = 0;
previous = float('inf')
for line in lines:
    current = int(line)
    if current > previous:
        count += 1
    previous = current
print("part1", filename, count)

count = 0
previous = float('inf')
for i in range(1, len(lines)-1, 1):
    current = int(lines[i-1]) + int(lines[i]) + int(lines[i+1])
    if current > previous:
        count += 1
    previous = current

print("part2", filename, count)