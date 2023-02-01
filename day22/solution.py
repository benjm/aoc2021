import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()

def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int
    z: int

ON="on"
OFF="off"

@dataclass
class Cube:
    id: str
    typ: str
    point0: Point
    point1: Point
    corners: set

    def containsPoint(self,point):
        if point.x < self.point0.x or point.x > self.point1.x:
            return False
        if point.y < self.point0.y or point.y > self.point1.y:
            return False
        if point.z < self.point0.z or point.z > self.point1.z:
            return False
        return True

    def containsCube(self,cube):
        p0 = cube.point0
        p1 = cube.point1
        if p0.x < self.point0.x or p1.x > self.point1.x:
            return False
        if p0.y < self.point0.y or p1.y > self.point1.y:
            return False
        if p0.z < self.point0.z or p1.z > self.point1.z:
            return False
        return True

    def overlaps(self, other):
        return any(self.containsPoint(p) for p in other.corners)

    def totalSize(self):
        point0=self.point0
        point1=self.point1
        return abs(point1.x - point0.x + 1) * abs(point1.y - point0.y + 1) * abs(point1.z - point0.z + 1)

def allCorners(xs,ys,zs):
    corners=set()
    for xi in range(2):
        for yi in range(2):
            for zi in range(2):
                corners.add(Point(xs[xi],ys[yi],zs[zi]))
    return corners

def processLines(lines):
    #on x=-49..1,y=-3..46,z=-24..28
    cubes=[]
    for cube_id in range(len(lines)):
        line = lines[cube_id]
        typ,coords=line.split()
        xs,ys,zs=map(lambda s: list(map(int,s.split("=")[1].split(".."))), coords.split(","))
        point0 = Point(min(xs),min(ys),min(zs))
        point1 = Point(max(xs),max(ys),max(zs))
        cube = Cube(str(cube_id),typ,point0,point1,allCorners(xs,ys,zs))
        cubes.append(cube)
    return cubes

def readFile(filename = sys.argv[1]):
    filename = sys.argv[1]
    lines = []
    with open(filename) as f:
        lines = f.read().splitlines()
    return processLines(lines)

cubes = readFile()
# for cube in cubes:
#     print(cube.id,cube.typ,cube.point0,cube.point1)

print(elapsedTimeMs(),"starting part1")
def pointIsOn(point, cubes):
    for cube in cubes[::-1]:
        if cube.containsPoint(point):
            return (cube.typ == ON)
    return False

def bruteForceCheck(low,hi,cubes):
    on=0
    on_points=set()
    n=0
    tot = abs(hi-low)**3
    for x in range(low,hi+1):
        for y in range(low,hi+1):
            for z in range(low,hi+1):
                n+=1
                if n%100000==0:
                    print(f"{elapsedTimeMs()} checking point {n} of {tot}")
                p = Point(x,y,z)
                if pointIsOn(p,cubes):
                    on+=1
                    on_points.add(p)
    print(f"{elapsedTimeMs()} found {on} ON within {low}..{hi} init cuboid")
    return on
print("skipping Part 1's bruteForceCheck...")
# bruteForceCheck(-50,50,cubes)
# 0:01:06.475375 found 607657 ON within

print(elapsedTimeMs(),"starting part2")
def containedByAny(cube, cubes):
    for other in cubes:
        if other.containsCube(cube):
            return True
    return False

def findOverlapping(cube, remaining):
    overlappers=[]
    for other in remaining:
        if other.overlaps(cube) or cube.overlaps(other): # need to check both ways in case of fully enclosed other
            overlappers.append((other.id,other.typ))
    return overlappers

# def countNonOverlappedCubes(cube_map,cube_id,overlapper_id_typs):
#     cube = cube_map[cube_id]
#     overlappers = list(cube_map[oid] for oid,otyp in overlapper_id_typs)
#     points = set()
#     sz = cube.totalSize()
#     c = 0
#     for x in range(cube.point0.x,cube.point1.x+1):
#         for y in range(cube.point0.y,cube.point1.y+1):
#             for z in range(cube.point0.z,cube.point1.z+1):
#                 p = Point(x,y,z)
#                 c+=1
#                 if c%1000000==0:
#                     print(f"\t{elapsedTimeMs()}up to point {c} out of {sz} points ...")
#                 if any(other.containsPoint(p) for other in overlappers):
#                     pass
#                 else:
#                     points.add(p)
#                 # HAHAHA ...    0:00:22.196073up to point Point(x=-47488, y=24810, z=35219) out of 200086456089240 points ...
#     return len(points)

def getIntersectCube(cube,other):
    # if (not other.overlaps(cube)) and (not cube.overlaps(other)):
    #     return None
    x1 = min(cube.point1.x, other.point1.x)
    y1 = min(cube.point1.y, other.point1.y)
    z1 = min(cube.point1.z, other.point1.z)

    x0 = max(cube.point0.x, other.point0.x)
    y0 = max(cube.point0.y, other.point0.y)
    z0 = max(cube.point0.z, other.point0.z)

    if x0>x1 or y0>y1 or z0>z1:
        return None

    point0 = Point(x0,y0,z0)
    point1 = Point(x1,y1,z1)
    intersect_id = f"({cube.id}:{other.id})"
    intersect = Cube(intersect_id, cube.typ, point0, point1, allCorners([x0,x1], [y0,y1], [z0,z1]))
    return intersect

# print("testing intersect")
# def genTestCube(cid,lo,hi,typ=ON):
#     return genTestCubeOther(cid,lo,lo,lo,hi,hi,hi, typ)

# def genTestCubeOther(cid,x0,y0,z0,x1,y1,z1,typ=ON):
#     return Cube(cid, typ, Point(x0,y0,z0), Point(x1,y1,z1), allCorners([x0,x1], [y0,y1], [z0,z1]))

# def testIntersect(a,b,s):
#     i = getIntersectCube(a,b)
#     r=f"\t==>\t{i}\n------------"
#     if i:
#         r=f"\t==>\t{i.point0}\t{i.point1}\n------------"
#     print(f"Intersection of {s}:\n\t{a.point0}--{a.point1}\t<i>\t{b.point0}--{b.point1}{r}")
#     print()

# def testBasicIntersect(lo1,hi1,lo2,hi2,s):
#     a = genTestCube(-1,lo1,hi1)
#     b = genTestCube(-2,lo2,hi2)
#     testIntersect(a,b,s)

# def testComplexIntersect(x0,y0,z0,x1,y1,z1, x2, y2, z2, x3, y3, z3, s):
#     a = genTestCubeOther(-1, x0, y0, z0, x1, y1, z1)
#     b = genTestCubeOther(-2, x2, y2, z2, x3, y3, z3)
#     testIntersect(a,b,s)

# testBasicIntersect(10,20,19,25,"corner")
# testBasicIntersect(10,20,20,25,"point")
# testBasicIntersect(10,20,12,14,"contained")
# testBasicIntersect(10,20,5,25,"surround")
# testBasicIntersect(10,20,40,50,"none")
# testComplexIntersect(10,10,10,20,20,20,12,12,5,14,14,25,"through centre")
# testComplexIntersect(10,10,10,20,20,20,12,12,5,14,14,15,"into side")
# testComplexIntersect(10,10,10,20,20,20,10,10,5,20,20,9,"none end-to-end")
# testComplexIntersect(10,10,10,20,20,20,5,5,5,15,10,15,"I think linear")
# exit()

def shatterCube(cube,other):
    if (not other.overlaps(cube)) and (not cube.overlaps(other)):
        return [cube]
    if other.containsCube(cube):
        return []
    subCubes=[]
    #print("TODO: shattering")
    intersectCube = getIntersectCube(cube,other)
    #print("TODO: or maybe clever add/subtract logic based on intersects")
    return subCubes

def findNonOverlappedSubCubes(cube_map,cube_id,overlapper_id_typs):
    originalCube = cube_map[cube_id]
    cubes = [originalCube]
    overlappers = list(cube_map[oid] for oid,otyp in overlapper_id_typs)
    for overlapper in overlappers:
        subCubes = []
        for cube in cubes:
            subCubes+=shatterCube(cube,overlapper)
        cubes = subCubes
    return cubes

def analyseCubes(cubes):
    cube_map={}
    for cube in cubes:
        cube_map[cube.id]=cube
    onWithOverlappers={}
    lastON=set()
    redundant=[]
    for i in range(len(cubes)-1):
        cube = cubes[i]
        remaining = cubes[i+1:]
        if containedByAny(cube, remaining):
            redundant.append(cube.id)
        elif cube.typ==ON:
            overlappers = findOverlapping(cube, remaining)
            if len(overlappers)==0:
                lastON.add(cube.id)
            else:
                onWithOverlappers[cube.id]=overlappers
    if cubes[-1].typ==ON:
        lastON.add(cubes[-1].id)
    print(f"# There are {len(cubes)} cubes, with {sum(c.typ==OFF for c in cubes)} OFF cubes")
    print(f"# There are {len(lastON)} ON cubes with no following overlappers")
    print(f"# There are {len(redundant)} redundant cubes that are completely overlapped by another")
    print(f"# There are {len(onWithOverlappers)} ON cubes with following overlappers:")
    hasOFFOverlapper=0
    allONOverlappers=0
    for cube_id in sorted(onWithOverlappers):
        overlappers = onWithOverlappers[cube_id]
        if any(typ==OFF for cube_id,typ in overlappers):
            hasOFFOverlapper+=1
        else:
            allONOverlappers+=1
    print(f"# \t{hasOFFOverlapper} of them include at least one OFF overlapper\n# \t{allONOverlappers} of them have only ON overlappers")
    print(f"{elapsedTimeMs()} starting to count...")

    totalOn = sum(cubes[int(cube_id)].totalSize() for cube_id in lastON)
    c = 0
    for cube in onWithOverlappers:
        c+=1
        if c%50==0:
            print(f"{elapsedTimeMs()} up to cube {c} of {len(onWithOverlappers)}")
        subCubes=findNonOverlappedSubCubes(cube_map,cube_id,onWithOverlappers[cube_id])
        totalOn+=sum(subCube.totalSize() for subCube in subCubes)
    print(f"{elapsedTimeMs()} ending analyseCubes")

analyseCubes(cubes)
# input onWithOverlappers:
# There are 420 cubes, with 105 OFF cubes
# There are 25 ON cubes with no following overlappers
# There are 11 redundant cubes that are completely overlapped by another
# There are 282 ON cubes with following overlappers:
#     226 of them include at least one OFF overlapper
#     56 of them have only ON overlappers

def determineTotalNotOverlapped(i,volume,intersectVolumes):
    if (i+1)>=len(cubes): # i.e. last cube, there are none that might intersect
        return volume
    overlapper_indeces = [j for j in range(i+1,len(cubes)) if intersectVolumes[(i,j)] > 0]
    # for 
    #     intersectVolume = 
    #     if intersectVolume>0:
    print("TODO: determineTotalNotOverlapped")
    return volume

def getIntersectVolumes(cubes):
    num_cubes = len(cubes)
    intersectVolumes={}
    for i in range(num_cubes-1):
        for j in range(i+1,num_cubes):
            intersectCube = getIntersectCube(cubes[i], cubes[j])
            intersectVolume = 0
            if intersectCube:
                intersectVolume = intersectCube.totalSize()
            intersectVolumes[(i,j)]=intersectVolume
            intersectVolumes[(j,i)]=intersectVolume
    return intersectVolumes

def combinedVolume(cubes,path=[]):
    if not cubes:
        return 0
    vol = 0
    for i in range(len(cubes)):
        cube = cubes[i]
        # indent="" + "\t"*len(path) + "-".join(map(str,path))
        # print(f"\t{indent}-({i+1}/{len(cubes)}) - {cube.id}")
        addVol = cube.totalSize()
        prev = []
        for prev_cube in cubes[:i]:
            prev_intersection = getIntersectCube(cube,prev_cube)
            if prev_intersection:
                prev.append(prev_intersection)
        subVol = combinedVolume(prev,path+[i])
        vol = vol + addVol - subVol
    return vol

# print("testing combined_volume")
def genTestCube(cid,lo,hi,typ=ON):
    return genTestCubeOther(cid,lo,lo,lo,hi,hi,hi, typ)

def genTestCubeOther(cid,x0,y0,z0,x1,y1,z1,typ=ON):
    return Cube(cid, typ, Point(x0,y0,z0), Point(x1,y1,z1), allCorners([x0,x1], [y0,y1], [z0,z1]))

# def testCombinedVolume():
#     cubes=[]
#     cubes.append(genTestCube(0,10,19))
#     cubes.append(genTestCube(0,19,28))
#     cubes.append(genTestCube(0,19,28))
#     cubes.append(genTestCube(0,19,29))
#     cubes.append(genTestCube(0,10,11))
#     v = combinedVolume(cubes)
#     print(f"combinedVol of {len(cubes)} is {v}")
#     for cube in cubes:
#         print(f"\t{cube.point0}\t{cube.point1}\t{cube.totalSize()}")
#     print()

# testCombinedVolume()
# exit()

def determineTotalOn(cubes):
    # 0:00:00.364503 returned 175980 intersection volumes for 420 cubes
    totalOn=0
    n,d=0,50
    for i in range(len(cubes)):
        cube = cubes[i]
        relevantVol=0
        if cube.typ==ON:
            n+=1
            if n%d==0:
                print(f"{elapsedTimeMs()} assessing ON cube #{n} (cube {i} out of {len(cubes)})")
            cubeVol=cube.totalSize()
            #volume of ON cube not overlapped by [overlappers]
            overlappers = []
            for other in cubes[i+1:]:
                intersectCube = getIntersectCube(cube, other)
                if intersectCube: # only interested in the part of the overlappers that intersect our baseline cube
                    overlappers.append(intersectCube)
            overlapVol = combinedVolume(overlappers,[i])
            #volume from [overlappers]
            relevantVol = cubeVol - overlapVol
            #for each overlapper:volume not overlapped by following overlapper
            # if n%d==0:
            #     print(f"\t{elapsedTimeMs()} done with {n}")
        totalOn+=relevantVol
    return totalOn

totalOn = determineTotalOn(cubes)
print(f"{elapsedTimeMs()} Total cubes on (using intersetion logic): {totalOn}")
# LOGIC:
# iterate up through cubes and, for every ON cube, count total ON that do not end up being overlapped by something (on or off) in any following cube

print(elapsedTimeMs(),"redoing part1 using intersection overlap logic")
def determineTotalOnUsingLimitedOnArea(cubes, limitingCube):
    trimmedCubes = []
    for cube in cubes:
        intersectCube = getIntersectCube(cube,limitingCube)
        if intersectCube:
            trimmedCubes.append(intersectCube)
    return determineTotalOn(trimmedCubes)

initOn = determineTotalOnUsingLimitedOnArea(cubes,genTestCube("init",-50,50,OFF))
print(f"{elapsedTimeMs()} Total cubes on within the bounded init space (using intersetion logic): {initOn}")

##TODO: clean up this lovely messy code to leave on ly the efficient intersection logic behind :)