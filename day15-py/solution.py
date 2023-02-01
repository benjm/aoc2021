import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()

@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int
    risk: int

@dataclass
class Cavern:
    width: int
    height: int
    points: dict

def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

def processLines(lines):
    height = len(lines)
    width = len(lines[0])
    points={}
    for y in range(height):
        for x in range(width):
            v = int(lines[y][x])
            points[(x,y)] = Point(x,y,v)
    return Cavern(width, height, points)

def readFile(filename = sys.argv[1]):
    filename = sys.argv[1]
    lines = []
    with open(filename) as f:
        lines = f.read().splitlines()
    return processLines(lines)

cavern = readFile()

print(elapsedTimeMs(),"starting part1")
def getNeighbours(path,cavern):
    neighbours = set()
    for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
        x = path.x + dx
        y = path.y + dy
        if 0<=x and x<cavern.width and 0<=y and y<cavern.height:
            neighbours.add(cavern.points[(x,y)])
    return neighbours

def leastRisk(cavern):
    print(f"walking through a cavern {cavern.width} wide and {cavern.height} high containing {len(cavern.points)} points")
    target=Point(cavern.width-1, cavern.height-1, math.inf)
    target_x_y = (target.x, target.y)
    paths=set()
    paths.add(Point(0,0,0))
    best={}
    best[(0,0)]=0
    n=0
    while len(paths) > 0:
        n+=1
        if n%10 == 0:
            print(f"{elapsedTimeMs()} iteration {n} is following {len(paths)} paths")
        new_paths = set()
        for path in paths:
            for neighbour in getNeighbours(path, cavern):
                neighbour_x_y=(neighbour.x, neighbour.y)
                new_path_risk = path.risk + neighbour.risk
                if new_path_risk < target.risk and new_path_risk < best.get(neighbour_x_y, target.risk):
                    new_path = Point(neighbour.x, neighbour.y, new_path_risk)
                    best[neighbour_x_y] = new_path.risk
                    new_paths.add(new_path)
                    if neighbour.x == target.x and neighbour.y == target.y and new_path.risk < target.risk:
                        target = new_path
        paths = new_paths
    return target

risk = leastRisk(cavern)
print(f"{elapsedTimeMs()} least risky path has a risk of {risk}")
print()
print(elapsedTimeMs(),"starting part2")
def expandCavern(cavern,print_out=False):
    points={}
    for x_y in cavern.points:
        x,y=x_y
        for mulx in range(5):
            for muly in range(5):
                xn=cavern.width*mulx+x
                yn=cavern.height*muly+y
                rn=cavern.points[x_y].risk+mulx+muly
                if rn>9:
                    rn-=9
                points[(xn,yn)]=Point(xn,yn,rn)
    return Cavern(cavern.width*5, cavern.height*5, points)

full_cavern = expandCavern(cavern)

risk = leastRisk(full_cavern)
print(f"{elapsedTimeMs()} least risky path has a risk of {risk}")
#0:00:17.230305 least risky path has a risk of Point(x=499, y=499, risk=2809)