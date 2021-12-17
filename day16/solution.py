import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

# test : 23
# operator packet which contains two sub-packets; each sub-packet is an operator packet that contains two literal values.
print("starting part1")
def tobinary(pkt):
    b = ""
    for c in list(pkt):
        b+=bin(int(c,16))[2:].zfill(4)
    return b

def tab(i):
    return i*"  "

# typ == 4 is a literal:
# groups of 5 bits, each msb=1 except last where msb=0, padded with trailing 0
#
# typ != 4 is an operator: contains one or more packets
# the bit immediately after the packet header denotes mode (lentgth type)
# 0: next 15 are a number = total length in bits of the sub-packets contained
# 1: next 11 are a number = number of sub-packets immediately contained
def literal(indent, pkt, nopadding):
    print(tab(indent),"LITERAL", pkt)
    cont = True
    i=0
    b=""
    while cont:
        five=pkt[i:i+5]
        i+=5
        b+=five[1:]
        cont=five[0]=="1"
    lit = int(b,2)
    if not nopadding:
        pad = 4 - ((i+6)%4)
        i+=pad
    print(tab(indent),"LITERAL",lit, pkt [:i])
    return [lit,pkt[i:]]

def containspkt(indent, pkt):
    check = len(pkt) > 0 and pkt.count("0") < len(pkt)
    print(tab(indent),"CHECK", check, pkt)
    return check

def multibits(indent, subpkt):
    print(tab(indent),"MULTI-BITS", len(subpkt))
    results=[]
    while containspkt(indent+1, subpkt):
        result,subpkt = decode(indent+1,subpkt,True)
        results.append(["SUBPACKET",result])
    return results

def multipkts(indent, pkt,n):
    print(tab(indent),"MULTI-PACKET", n, pkt)
    sz = len(pkt)
    results=[]
    for i in range(n):
        result,pkt = decode(indent, pkt, True)
        results.append(["SUBPACKET",result])
    sz = sz - len(pkt)
    return sz, results

def operator(indent, pkt, nopadding):
    print(tab(indent),"OPERATOR", pkt)
    mode=pkt[0]
    i=1
    results=[]
    if mode == "0":
        nbits = int(pkt[i:i+15],2)
        print(tab(indent),"NBITS",nbits, pkt)
        i+=15
        results = multibits(indent+1, pkt[i:i+nbits])
        pkt = pkt[i+nbits:]
    else:
        npkts = int(pkt[i:i+11],2)
        print(tab(indent),"NPKTS",npkts, pkt)
        i+=11
        sz,results = multipkts(indent+1, pkt[i:],npkts)
        pkt = pkt[i+sz:]

    ##??what about trailing zeros??
    i=0
    while len(pkt) > i and pkt[i] == "0":
        i+=1
    if i>0:
        #pkt=pkt[i:]
        print(tab(indent),"trailing zeros", i)
    
    v=sum(map(lambda r:r[1],results))
    print(tab(indent),"operator n,mode,vsum:", len(results), mode, v)
    return [v,pkt]

def decode(indent, pkt, nopadding):
    print(tab(indent),"PACKET", pkt)
    ver = int(pkt[:3],2)
    typ = int(pkt[3:6],2)
    if typ == 4:
        l,pkt=literal(indent+1,pkt[6:],nopadding)
    else:
        vsum,pkt=operator(indent+1,pkt[6:],nopadding)
        ver+=vsum
    print(tab(indent),"packet vsum:", ver)
    return [ver, pkt]

print("HEX:",lines[0])
packet = tobinary(lines[0])
print("BIN:",packet)
versionsum,pkt = decode(0,packet, False)

print("version sum", versionsum, pkt)

# print("starting part2")