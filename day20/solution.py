import sys
filename = sys.argv[1]
lines = []
with open(filename) as f:
    lines = f.read().splitlines()

algo=lines[0]
img = lines[2:]
one = "#"
zero = "."

print("starting part1")

def enhancepixel(y,x,img, default):
    h = len(img)
    w = len(img[0])
    b=""
    for yy in range(y-1,y+2):
        for xx in range(x-1,x+2):
            c=""
            if yy < 0 or yy >= h or xx < 0 or xx >= w:
                c=default
            else:
                c=img[yy][xx]
            b+=["1","0"][c==zero]
    return int(b,2)

def enhanceimg(img, default):
    h = len(img)
    w = len(img[0])
    o = [""]*(h+2)
    for y in range(-1,h+1):
        for x in range(-1,w+1):
            p = enhancepixel(y,x,img, default)
            o[y+1]+=algo[p]

    if default == zero and algo[0] == one:
        default = one
    elif default == one and algo[511] == zero:
        default=zero
    return o,default

default = zero
for i in range(50):
    print("ENHANCING "+str(i))
    img,default = enhanceimg(img,default)

count = 0
for i in range(len(img)):
    count += img[i].count(one)
    print(img[i])
print(count) # 4873 for x2 enhances and 16394 for x50

# print("starting part2")