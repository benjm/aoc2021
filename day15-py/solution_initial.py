import sys
import math
from dataclasses import dataclass
from datetime import datetime

datetime_start = datetime.now()

@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int

@dataclass
class Path:
    points: list
    risk: int

@dataclass
class Cavern:
    width: int
    height: int
    risk_map: dict

def elapsedTimeMs(since=datetime_start):
    return datetime.now()-since

def processLines(lines):
    height = len(lines)
    width = len(lines[0])
    risk_map = {}
    for y in range(height):
        for x in range(width):
            v = int(lines[y][x])
            risk_map[Point(x,y)]=v
    return Cavern(width, height, risk_map)

def readFile(filename = sys.argv[1]):
    filename = sys.argv[1]
    lines = []
    with open(filename) as f:
        lines = f.read().splitlines()
    return processLines(lines)

cavern = readFile()

print(elapsedTimeMs(),"starting part1")
def getNeighbours(point,cavern):
    points = []
    for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
        x = point.x + dx
        y = point.y + dy
        if 0<=x and x<cavern.width and 0<=y and y<cavern.height:
            points.append(Point(x,y))
    return points

def leastRisk(cavern,start,target):
    print(f"walking through a cavern {cavern.width} wide and {cavern.height} high")
    best={}
    best[start]=Path([start], 0)
    paths=[Path([start], 0)]
    n=0
    max_allowed = math.inf
    max_risk_seen=0
    while len(paths) > 0:
        n+=1
        if n%10 == 0:
            print(f"{elapsedTimeMs()} iteration {n} is following {len(paths)} paths")
        if target in best:
            max_allowed = best[target].risk
        new_paths = []
        for path in paths:
            for neighbour in getNeighbours(path.points[-1], cavern):
                point_risk = cavern.risk_map[neighbour]
                path_risk = path.risk + point_risk
                if path_risk < max_allowed:
                    if neighbour not in best or path_risk < best[neighbour].risk:
                        new_points = path.points.copy()
                        new_points.append(neighbour)
                        new_path = Path(new_points, path_risk)
                        new_paths.append(new_path)
                        best[neighbour] = new_path
                        if path_risk > max_risk_seen:
                            max_risk_seen = path_risk
        paths = new_paths
    return best[target]

start=Point(0,0)
target=Point(cavern.width-1, cavern.height-1)
best_path = leastRisk(cavern,start,target)
print(f"{elapsedTimeMs()} least risky path has a risk of {best_path.risk}")
print()
print(elapsedTimeMs(),"starting part2")
def expandCavern(cavern,print_out=False):
    risk_map={}

    for y_mult in range(5):
        if print_out: print()
        for y in range(cavern.height):
            if print_out: row=""
            for x_mult in range(5):
                if print_out: row+=" "
                for x in range(cavern.width):
                    expanded_x = cavern.width * x_mult + x
                    expanded_y = cavern.height * y_mult + y
                    expanded_point=Point(expanded_x, expanded_y)
                    expanded_v = cavern.risk_map[Point(x,y)] + x_mult + y_mult
                    if expanded_v > 9:
                        expanded_v-=9
                    risk_map[expanded_point] = expanded_v
                    if print_out: row+=str(expanded_v)
            if print_out: print(" ".join(list(row)))
    return Cavern(cavern.width*5, cavern.height*5, risk_map)

full_cavern = expandCavern(cavern)
target=Point(full_cavern.width-1, full_cavern.height-1)
best_path = leastRisk(full_cavern,start,target)
#gave up after 1:11:47.631453 iteration 650 is following 419137 paths (maybe on its way back down ... so probably <3 hours but actual solution took <20s :P)
print(f"{elapsedTimeMs()} least risky path has a risk of {best_path.risk}")