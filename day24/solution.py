import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()

def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

# The ALU is a four-dimensional processing unit: it has integer variables w, x, y, and z. These variables all start with the value 0. The ALU also supports six instructions:
# inp a - Read an input value and write it to variable a.
# add a b - Add the value of a to the value of b, then store the result in variable a.
# mul a b - Multiply the value of a by the value of b, then store the result in variable a.
# div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
# mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
# eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.
# it will indicate that the model number was valid by leaving a 0 in variable z
# Submarine model numbers are always fourteen-digit numbers consisting only of digits 1 through 9. The digit 0 cannot appear in a model number.
# e.g. 13579246899999

W, X, Y, Z = "w", "x", "y", "z"
def initRegistersInt():
    return {W:0, X:0, Y:0, Z:0}
def initRegistersStr():
    return {W:"0", X:"0", Y:"0", Z:"0"}

INP,ADD,MUL,DIV,MOD,EQL="inp add mul div mod eql".split()

@dataclass
class Instruction:
    op: str
    a: str
    b: str
    def run(self,reg):
        A = reg[self.a]
        B = None
        if self.b in [W,X,Y,Z]:
            B = reg[self.b]
        else:
            B = int(self.b)
        if self.op==INP: reg[self.a] = B
        elif self.op==ADD: reg[self.a] = reg[self.a] + B
        elif self.op==MUL: reg[self.a] = reg[self.a] * B
        elif self.op==DIV:
            if B==0:
                raise Exception(f"ERROR DIV {reg[self.a]} // {B}")
            reg[self.a] = reg[self.a] // B
        elif self.op==MOD: reg[self.a] = reg[self.a] % B
        elif self.op==EQL: reg[self.a] = int(reg[self.a] == B)
        return reg

def processLines(lines):
    instructions = []
    for line in lines:
        op, *ab = line.split()
        if len(ab)==1:
            instructions.append(Instruction(op,ab[0],None))
        else:
            instructions.append(Instruction(op,ab[0],ab[1]))
    return instructions

def readFile(filename = sys.argv[1]):
    filename = sys.argv[1]
    lines = []
    with open(filename) as f:
        lines = f.read().splitlines()
    return processLines(lines)

instructions = readFile()

print(elapsedTimeMs(),"starting part1")
def testNumber(instructions, model_number, printing=False):
    model_number_array = list(str(model_number))
    testNumberArray(instructions, model_number_array, printing)

def testNumberArray(instructions, model_number_array, printing=False):
    if len(model_number_array) != 14:
        print("ERROR, modelnumber must be exactly 14 digits long")
        exit()
    reg = initRegistersInt()
    i=0
    while i < 14:
        for instruction in instructions:
            if instruction.op == INP:
                instruction.b = model_number_array[i]
                i+=1
            try:
                reg = instruction.run(reg)
            except Exception as e:
                print(e)
    if printing:
        print(f"{elapsedTimeMs()} test run with model_number {model_number_array} resulted in z={reg[Z]}")
        if reg[Z] == 0:
            print(f"\tVALID: {''.join(model_number_array)}")
        else:
            print(f"\tINVALID (Z={reg[Z]}):{''.join(model_number_array)}")
            # raise Exception(f"invalid model_number_array {model_number_array}")
    return reg[Z] == 0

testNumber(instructions, 13579246899999, True)

def bracket(x):
    if len(x) == 1 or x.isdigit():
        return x
    return "( "+x+" )"

def evaluateOp(op, lhs, rhs):
    if op == INP: return rhs
    if lhs.isdigit() and rhs.isdigit():
        if op == ADD: return str(int(lhs)+int(rhs))
        elif op == MUL:
            if lhs == "0" or rhs == "0": return "0"
            return str(int(lhs)*int(rhs))
        elif op == DIV: return str(int(lhs)//int(rhs))
        elif op == MOD: return str(int(lhs)%int(rhs))
        elif op == EQL: return str(int(int(lhs)==int(rhs)))
    if op==ADD:
        if lhs.isdigit() and int(lhs)==0:
            return rhs
        elif rhs.isdigit() and int(rhs)==0:
            return lhs
        if rhs.startswith("-") and rhs[1:].isdigit() and int(rhs)<0:
            return bracket(lhs) + " - " + str(abs(int(rhs)))
        return bracket(lhs) + " + " + rhs
    elif op==MUL:
        if lhs == "0" or rhs == "0":
            return "0"
        return bracket(lhs) + " * " + bracket(rhs)
    elif op==DIV:
        if rhs == "1":
            return lhs
        return bracket(lhs) + " // " + bracket(rhs)
    elif op==MOD:
        if rhs == "1":
            return "0"
        return bracket(lhs) + " % " + bracket(rhs)
    elif op==EQL:
        if lhs==rhs:
            return "1"
        return bracket(lhs) + " == " + bracket(rhs)
    raise Exception(f"Unknown op {op}")

def expandInstructions(instructions):
    inp_c = ord('A')
    reg = initRegistersStr()
    expandedI=""
    while inp_c < ord('A') + 14:
        for instruction in instructions:
            # insert input variable
            if instruction.op == INP:
                i = inp_c - ord('A') - 1
                if i>=0:
                    print(f"# {chr(inp_c-1)} {str(i).rjust(2)}: Z = {reg[Z]}")
                    reg={W:"W", X:"X", Y:"Y", Z:"Z"}
                instruction.b = chr(inp_c)
                inp_c+=1
            # get rhs value
            rhs = instruction.b
            if instruction.b in [W,X,Y,Z]:
                rhs = reg[instruction.b]
            # update registers
            try:
                reg[instruction.a] = evaluateOp(instruction.op, reg[instruction.a], rhs)
            except:
                print(f"failed in evaluating {instruction.op}, {reg[instruction.a]}, {rhs}")
    print(f"# {chr(inp_c-1)} {str(inp_c - ord('A') - 1).rjust(2)}: Z = {reg[Z]}")
    return expandedI,reg

for i in range(1,10):
    r = (-i-8)*26 + i + 7
    print("Z(M)",i,"\t",r,"\t",r//26,r%26)

expandedI,reg = expandInstructions(instructions)

# A  0: Z = ( A + 4 ) * ( ( 12 == A ) == 0 )
# # A is in range 1..9 so rhs always equates to 1, which collapses to Z = A + 4
# B  1: Z = (   Z         * ( ( 25 * ( ( ( ( Z % 26 ) + 11 ) == B ) == 0 ) ) + 1 ) ) + ( B + 10 ) * ( ( ( ( Z % 26 ) + 11 ) == B ) == 0 )
# # B is in the range 1..9 so rhs always equates to 1 and Z = 
# C  2: Z = (   Z         * ( ( 25 * ( ( ( ( Z % 26 ) + 14 ) == C ) == 0 ) ) + 1 ) ) + ( C + 12 ) * ( ( ( ( Z % 26 ) + 14 ) == C ) == 0 )
# D  3: Z = ( ( Z // 26 ) * ( ( 25 * ( ( ( ( Z % 26 ) -  6 ) == D ) == 0 ) ) + 1 ) ) + ( D + 14 ) * ( ( ( ( Z % 26 ) -  6 ) == D ) == 0 )
# E  4: Z = (   Z         * ( ( 25 * ( ( ( ( Z % 26 ) + 15 ) == E ) == 0 ) ) + 1 ) ) + ( E +  6 ) * ( ( ( ( Z % 26 ) + 15 ) == E ) == 0 )
# F  5: Z = (   Z         * ( ( 25 * ( ( ( ( Z % 26 ) + 12 ) == F ) == 0 ) ) + 1 ) ) + ( F + 16 ) * ( ( ( ( Z % 26 ) + 12 ) == F ) == 0 )
# G  6: Z = ( ( Z // 26 ) * ( ( 25 * ( ( ( ( Z % 26 ) -  9 ) == G ) == 0 ) ) + 1 ) ) + ( G +  1 ) * ( ( ( ( Z % 26 ) -  9 ) == G ) == 0 )
# H  7: Z = (   Z         * ( ( 25 * ( ( ( ( Z % 26 ) + 14 ) == H ) == 0 ) ) + 1 ) ) + ( H +  7 ) * ( ( ( ( Z % 26 ) + 14 ) == H ) == 0 )
# I  8: Z = (   Z         * ( ( 25 * ( ( ( ( Z % 26 ) + 14 ) == I ) == 0 ) ) + 1 ) ) + ( I +  8 ) * ( ( ( ( Z % 26 ) + 14 ) == I ) == 0 )
# J  9: Z = ( ( Z // 26 ) * ( ( 25 * ( ( ( ( Z % 26 ) -  5 ) == J ) == 0 ) ) + 1 ) ) + ( J + 11 ) * ( ( ( ( Z % 26 ) -  5 ) == J ) == 0 )
# K 10: Z = ( ( Z // 26 ) * ( ( 25 * ( ( ( ( Z % 26 ) -  9 ) == K ) == 0 ) ) + 1 ) ) + ( K +  8 ) * ( ( ( ( Z % 26 ) -  9 ) == K ) == 0 )
# L 11: Z = ( ( Z // 26 ) * ( ( 25 * ( ( ( ( Z % 26 ) -  5 ) == L ) == 0 ) ) + 1 ) ) + ( L +  3 ) * ( ( ( ( Z % 26 ) -  5 ) == L ) == 0 )
# M 12: Z = ( ( Z // 26 ) * ( ( 25 * ( ( ( ( Z % 26 ) -  2 ) == M ) == 0 ) ) + 1 ) ) + ( M +  1 ) * ( ( ( ( Z % 26 ) -  2 ) == M ) == 0 )
# N 13: Z = ( ( Z // 26 ) * ( ( 25 * ( ( ( ( Z % 26 ) -  7 ) == N ) == 0 ) ) + 1 ) ) + ( N +  8 ) * ( ( ( ( Z % 26 ) -  7 ) == N ) == 0 )

# # theorising manually - not .py but useful for bracket matching

# A  0: Z = A + 4
# B  1: Z = ( A + 4 ) * 26 + B + 10
# C  2: Z = ( ( A + 4 ) * 26 + B + 10 ) * 26 + C + 12
# D  3: Z = ( A + 4 ) * 26 + B + 10
# E  4: Z = ( ( A + 4 ) * 26 + B + 10 ) * 26 + E +  6
# F  5: Z = ( ( ( A + 4 ) * 26 + B + 10 ) * 26 + E +  6 ) * 26 + F + 16
# G  6: Z = ( ( A + 4 ) * 26 + B + 10 ) * 26 + E +  6
# H  7: Z = ( ( ( A + 4 ) * 26 + B + 10 ) * 26 + E +  6 ) * 26 + H +  7
# I  8: Z = ( ( ( ( A + 4 ) * 26 + B + 10 ) * 26 + E +  6 ) * 26 + H +  7 ) * 26 + I +  8
# J  9: Z = ( ( ( A + 4 ) * 26 + B + 10 ) * 26 + E +  6 ) * 26 + H +  7
# K 10: Z = ( ( A + 4 ) * 26 + B + 10 ) * 26 + E +  6
# L 11: Z = ( A + 4 ) * 26 + B + 10
# M 12: Z = ( A + 4 )
# N 13: Z = ( N + 8 ) * ( ( A - 3 == N ) == 0 )

# # UGH ... really confused ... some good discussion here:
# # https://www.reddit.com/r/adventofcode/comments/rnejv5/2021_day_24_solutions/

# # 14 equations, 7 increase the value, 7 decrease it
# # each row is either (Z//1) multiplied by 26 or, in order that the value decreases, divided by 26 (i.e. not multiplied again)

# # gives the following relationship requirements for number ABCDEFGHIJKLMN
# C + 6 == D
# F + 7 == G
# I + 3 == J
# H - 2 == K
# E + 1 == L
# B + 8 == M
# A - 3 == N

def maxUsingPairing(instructions):
    b = 1
    m = 9
    tried=0
    for a in range(9,3,-1):
        n = a - 3
        print(f"{elapsedTimeMs()} next a {a} (min=4)")
        for c in range(3,0,-1):
            d = c + 6
            for e in range(8,0,-1):
                l = e + 1
                for f in range(2,0,-1):
                    g = f + 7
                    for h in range(9,2,-1):
                        k = h - 2
                        for i in range(6,0,-1):
                            j = i + 3
                            model_number_array_ints=[a,b,c,d,e,f,g,h,i,j,k,l,m,n]
                            tried+=1
                            if any(q>9 or q<1 for q in model_number_array_ints):
                                raise Exception(f"something broke: {model_number_array_ints}")
                            model_number_array=list(map(str,model_number_array_ints))
                            if testNumberArray(instructions, model_number_array):
                                print(f"{elapsedTimeMs()} found a result after {tried} checks")
                                return ''.join(model_number_array)
    raise Exception(f"something went wrong... tried {tried} variations of input")

def minUsingPairing(instructions):
    #this feels dirty ... :)
    b = 1
    m = 9
    tried=0
    for a in range(4,10):
        n = a - 3
        print(f"{elapsedTimeMs()} next a {a} (max=9)")
        for c in range(1,4):
            d = c + 6
            for e in range(1,9):
                l = e + 1
                for f in range(1,3):
                    g = f + 7
                    for h in range(3,10):
                        k = h - 2
                        for i in range(1,7):
                            j = i + 3
                            model_number_array_ints=[a,b,c,d,e,f,g,h,i,j,k,l,m,n]
                            tried+=1
                            if any(q>9 or q<1 for q in model_number_array_ints):
                                raise Exception(f"something broke: {model_number_array_ints}")
                            model_number_array=list(map(str,model_number_array_ints))
                            if testNumberArray(instructions, model_number_array):
                                print(f"{elapsedTimeMs()} found a result after {tried} checks")
                                return ''.join(model_number_array)
    raise Exception(f"something went wrong... tried {tried} variations of input")

res = maxUsingPairing(instructions)
print(f"{elapsedTimeMs()} using pairing: {res} was the first valid number found")
# 0:00:00.000942 found a result after 1 checks
# 0:00:00.000946 using pairing: 91398299697996 was the first valid number found

res = minUsingPairing(instructions)
print(f"{elapsedTimeMs()} using pairing: {res} was the first valid number found")
# 0:00:00.001083 found a result after 1 checks
# 0:00:00.001086 using pairing: 41171183141291 was the first valid number found

# def bruteForce():
#     model_number_array=[]
#     for i in range(14):
#         model_number_array.append(9)
#     found = 0
#     while not found:
#         try:
#             testNumberArray([map(str,model_number_array)])
#             found=1
#         except:
#             i = 13
#             model_number_array[i]-=1
#             while model_number_array[i]<1:
#                 model_number_array[i]=9
#                 i-=1
#                 model_number_array[i]-=1
#             if i == 6:
#                 print(f"{elapsedTimeMs()} down to {model_number_array}")
#     print(f"{elapsedTimeMs()} found {model_number_array} that seems to work")
#     # 0:00:32.845403 down to [9, 9, 9, 9, 9, 8, 8, 9, 9, 9, 9, 9, 9, 9] ... not brute force

# print(elapsedTimeMs(),"starting part2")
