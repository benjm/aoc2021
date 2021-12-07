import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().split('\n')

print("starting part1")
bits = len(lines[0])
count = [0]*bits
for line in lines:
    for i in range(bits):
        count[i] += [1,-1][line[i] == "0"]

epsilon = ""
gamma = ""

for b in count:
    if b > 0:
        epsilon += "1"
        gamma += "0"
    elif b < 0:
        epsilon += "0"
        gamma += "1"
    else:
        print("ERROR", count)

power = int(epsilon, 2) * int(gamma, 2)

print("power = " + str(power))

print("starting part2")

oxy = lines
co2 = lines

for i in range(bits):
    # most common in oxy
    ones = []
    zeros = []
    if len(oxy) > 1:
        for entry in oxy:
            if entry[i] == "1":
                ones.append(entry)
            else:
                zeros.append(entry)
        if len(ones) >= len(zeros):
            oxy = ones
        else:
            oxy = zeros
    # least common in co2
    ones = []
    zeros = []
    if len(co2) > 1:
        for entry in co2:
            if entry[i] == "1":
                ones.append(entry)
            else:
                zeros.append(entry)
        if len(ones) < len(zeros):
            co2 = ones
        else:
            co2 = zeros

print(oxy, co2, int(oxy[0], 2)*int(co2[0],2))


