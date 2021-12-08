import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.readlines()

print("starting part1")

count = 0
for line in lines:
    left,right = line.split(" | ")
    for length in map(len,right.split()):
        if length in [2,3,4,7]:
            count+=1

print("count(1,4,7,8) = ",count) # 390 for input

print("starting part2")

# [0,1,2,3,4,5,6,7,8,9] numbers
# [6,2,5,5,4,5,6,3,7,6] number of segments
# [1,7,4,(2,3,5),(0,6,9),8]
# [2,3,4,(5,5,5),(6,6,6),8]
# len5: 2,3,5 --> 3 only one to contain all of 1
# len6: 0,6,9 --> 6 only one not to contain all of 1 (==c)
# numLetters = [abcefg,cf,acdeg,acdfg,bcdf,abdfg,abdefg,acf,abcdefg,abcdfg]
# a is difference between 1 and 7
# g is difference between 9 and 4+a
# e is difference between 8 and 4+a+g (or only one not in 9)

total = 0
for line in lines:
    nmap={}
    left,right = line.split(" | ")
    pattern = []
    for pi in sorted(left.split(),key=len):
        pattern.append(''.join(sorted(pi)))

    one=pattern[0]
    nmap[one] = 1
    nmap[pattern[1]] = 7
    nmap[pattern[2]] = 4
    nmap[pattern[9]] = 8

    izeroornine = []
    csegment = "x"
    for i in range(6,9):
        pi=pattern[i]
        if (one[0] in pi) + (one[1] in pi) == 1:
            nmap[pi] = 6
            for c in "abcdefg":
                if c not in pi:
                    csegment = c
        else:
            izeroornine.append(i)
    two = ""
    three = ""
    for i in range(3,6):
        pi=pattern[i]
        if (one[0] in pi) and (one[1] in pi):
            nmap[pi] = 3
            three = pi
        elif csegment in pi:
            nmap[pi] = 2
            two = pi
        else:
            nmap[pi] = 5

    # the segment in 2 not in 3 is e
    esegment = "x"
    for c in two:
        if c not in three:
            esegment = c

    for i in izeroornine:
        pi = pattern[i]
        if esegment in pi:
            nmap[pi] = 0
        else:
            nmap[pi] = 9

    # all digits mapped
    valuestring = ""
    for c in right.split():
        k = ''.join(sorted(c))
        valuestring+=str(nmap[k])
    value = int(valuestring)
    total+=value

print("total = ", total)