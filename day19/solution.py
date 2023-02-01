import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()

def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

@dataclass
class Scanner:
    name: str
    beacons: set

@dataclass(unsafe_hash=True)
class Beacon:
    x: int
    y: int
    z: int

def processScanner(lines, i):
    if i > len(lines)-1 or len(lines[i])==0:
        i+=1
        return None,i
    scanner_id = " ".join(lines[i].split()[1:3])
    i+=1
    beacons=set()
    while i<len(lines) and len(lines[i])>0:
        x,y,z=map(int,lines[i].split(","))
        beacons.add(Beacon(x,y,z))
        i+=1
    return Scanner(scanner_id, beacons),i

def processLines(lines):
    scanners=[]
    i=0
    while i<len(lines):
        scanner,i = processScanner(lines,i)
        if scanner:
            scanners.append(scanner)
    return scanners

def readFile(filename = sys.argv[1]):
    filename = sys.argv[1]
    lines = []
    with open(filename) as f:
        lines = f.read().splitlines()
    return processLines(lines)

scanners = readFile()

print(elapsedTimeMs(),"starting part1")

def modifyXYZ(xyz,up,rot):
    x,y,z=xyz
    if up == 1:
        x,y,z = -z,y,x
    elif up == 2:
        x,y,z = x,-z,y
    elif up == 3:
        x,y,z = z,y,-x
    elif up == 4:
        x,y,z = x,z,-y
    elif up == 5:
        x,y,z = -x,y,-z
    #rotate
    while rot>0:
        rot-=1
        x,y,z = -y,x,z
    return (x,y,z)

# def testOrientations(xyz):
#     results={}
#     for up in range(6):
#         for rot in range(4):
#             mod_xyz = modifyXYZ(xyz,up,rot)
#             result = results.get(mod_xyz, [])
#             result.append((up,rot))
#             results[mod_xyz] = result
#     return results

# xyz0=(1,2,3)
# orient=testOrientations(xyz0)
# print(f"testing orientations of {xyz0} ... found {len(orient)}")
# for xyz in orient:
#     print(f"\t{xyz} ... {orient[xyz]}")
# exit()

def rotateScanner(scanner, up, rot):
    rotated_id = scanner.name+f" U/R:({up}/{rot})"
    beacons=set()
    for b in scanner.beacons:
        x,y,z = modifyXYZ((b.x, b.y, b.z), up, rot)
        beacons.add(Beacon(x,y,z))
    return Scanner(rotated_id, beacons)

def shiftScanner(scanner, b_from, b_to):
    xyzdelta=(b_to.x-b_from.x, b_to.y-b_from.y, b_to.z-b_from.z)
    shifted_id = scanner.name+f" Shift {xyzdelta}"
    dx,dy,dz=xyzdelta
    beacons = set()
    for b in scanner.beacons:
        x = b.x+dx
        y = b.y+dy
        z = b.z+dz
        beacons.add(Beacon(x,y,z))
    return Scanner(shifted_id, beacons), xyzdelta

def getOverlaps(other, scanner, need):
    remain = len(other.beacons)
    same = set()
    for bm in other.beacons:
        if bm in scanner.beacons:
            same.add(bm)
        if remain + len(same) < need:
            return None
        if len(same) >= need:
            return same
        remain-=1
    return None

NEED=12

def checkOverlap(scanner, other, up, rot):
    rotated = rotateScanner(other, up, rot)
    for bf in rotated.beacons:
        #try aligning each beacon in rotated to each beacon in scanner and see how many overlaps
        for bs in scanner.beacons:
            moved,xyzdelta = shiftScanner(rotated, bf, bs)
            same = getOverlaps(moved,scanner,NEED)
            if same:
                return (moved,xyzdelta,up,rot,same)
    return None

def checkAllOverlaps(scanner, other):
    #each scanner could be in any of 24 different orientations: facing positive or negative x, y, or z, and considering any of four directions "up" from that facing.
    for up in range(6):
        for rot in range(4):
            overlap = checkOverlap(scanner, other, up, rot)
            if overlap:
                return overlap
    #print(f"no overlap found between {scanner.name} and {other.name}")
    return None

def mergeScanners(scanners):
    scanner0 = scanners[0]
    remaining = scanners[1:].copy()
    scanner_xyz=[(0,0,0)]
    while len(remaining) > 0:
        print(f"{elapsedTimeMs()} there are {len(remaining)} scanners left to merge")
        no_overlaps=[]
        for other in remaining:
            overlap = checkAllOverlaps(scanner0, other)
            if overlap:
                transformed,xyzdelta,up,rot,same = overlap
                scanner0.name+="+"+transformed.name.split()[1]
                scanner0.beacons.update(transformed.beacons)
                print(f"found overlap. {other.name} is at {xyzdelta} relative to {scanner0.name}, which now has {len(scanner0.beacons)}")
                scanner_xyz.append(xyzdelta)
                # print("\tOverlapping beacons:")
                # for b in same:
                #     print(f"\t{b}")
            else:
                no_overlaps.append(other)
        if len(remaining)==len(no_overlaps):
            print(f"ERROR - didn't find any more to merge :( still have {[s.name for s in remaining]}")
            # print(scanner0.name,"beacons:")
            # for b in sorted(scanner0.beacons,key=lambda b:b.x):
            #     print(b)
            exit()
        remaining = no_overlaps
    return scanner0,scanner_xyz

mega_scanner,scanner_xyz = mergeScanners(scanners)
print(f"{elapsedTimeMs()} merged {len(scanners)} scanners into a single one with {len(mega_scanner.beacons)} beacons")

print(elapsedTimeMs(),"starting part2")
def calcMHDist(xyz0, xyz1):
    x0,y0,z0=xyz0
    x1,y1,z1=xyz1
    return abs(x1-x0) + abs(y1-y0) + abs(z1-z0)

def manhattanDist(scanner_xyz):
    distances = set()
    for i in range(len(scanner_xyz)-1):
        for j in range(i+1,len(scanner_xyz)):
            dist = calcMHDist(scanner_xyz[i], scanner_xyz[j])
            distances.add(dist)
    return max(distances)

max_distance = manhattanDist(scanner_xyz)
print(f"{elapsedTimeMs()} Max MH Dist: {max_distance}")
