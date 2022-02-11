# - i-map

import random
import os

# - Lists of rectangles
shapes1 = {
    1:{"x": 3, "y": 3},
}

symbols = {
    "land": "^",
    "forest": "*",
    "lake": "_",
    "river": " ",
    "city": "!",
    "gold" : "@",
    "mountain" : "M",
}

# Function that creates the basic map, defines stuff like size, legend, positions on left/right side, ect
def Start():
    global MAP
    global stuff
    global PIL
    global Legend
    global shapes
    global l
    global a
    global b
    global A
    global c
    global LS
    global RS
    global p
    stuff = ["*", "@", "!", ".", "+", "%", "&", "$", "#"]
    PIL = []
    MAP = {}
    shapes = shapes1
    l = 15
    c = 3
    size = os.get_terminal_size()
    a = size.lines - 3
    b = size.columns - 25
    p = "T"
    A = a*b
    MAP = {}
    for x in range(A):
        MAP[x] = symbols["land"]
    RS = [b]
    LS = [0]
    i = 0
    y = 0
    while i != a:
        y += b
        LS.append(y)
        i += 1
    i = 0
    y = 0
    while i != a:
        y += b
        RS.append(y)
        i += 1

# Functions that name stuff
def Namer():
    FP = random.choice(["东","南","西","北", "前", "后", "江"])
    SP = random.choice(["秦","楚","齐","燕", "赵", "魏", "韩", "汉", "吴", "越", "宋", "晋", "唐", "明", "元"])
    return FP + SP

def Hnamer():
    FP = random.choice(["Mikker","Wimmly","Jarmit", "FiFyFo", "Peeter", "Nipnoe", "Padfot", "??????"])
    SP = random.choice(["Bold  |","Stong |","Fast  |","Large |", "Small |", "Fat   |", "Stuped|", "Smart |", "Fine  |"])
    return FP + " the " + SP

def Dnamer():
    return random.choice(["Scar             |","Kainto           |","Flea             |", "Botron           |", "Frot             |", "Clotenomen       |", "Fimotrin         |", "Death            |"])

# Function that prints the map to the console
def PrintM():
    global a
    global b
    global MAP
    global Legend
    c = 0
    x = 0
    i = 0
    for i in range(a):
        for x in range(b):
            print(MAP[c], end = "")
            x += 1
            c += 1
        try:
            print(Legend[i])
        except:
            print(" |                      |")
        x = 1
        i += 1

# Function that places Box on x
def PlaceB(i):
    global Box
    global a
    global b
    global MAP
    y = 0
    x = 0
    while y != shapes[Box]["y"]:
        while x != shapes[Box]["x"]:
            MAP[i] = "#"
            i +=1
            x += 1
            if i%b == 0:
                break
        i += (b - shapes[Box]["x"])
        y += 1
        x = 0
        if i >= A:
            break


def PickLocations(begin, end):
   global Points
   begin_row = int(begin/b) 
   begin_column = begin - begin_row * b
   end_row = int(end/b)
   end_column = end - end_row * b

   mid_row = int((begin_row + end_row) / 2)
   mid_column = int((begin_column + end_column) / 2)
   print(mid_row, mid_column)
   mid = mid_row * b + mid_column
   if ((mid_row == begin_row) and (mid_column == begin_column)) or (mid in Points) :
       return
   else:
       Points.append(mid)
       PickLocations(begin, mid)
       PickLocations(mid, end)

# Function that design which locations to place box
def DesignLocations():
    global A
    global a
    global b
    global Points
    Points = []
    Points.append(0)
    Points.append(A - 1)
    PickLocations(0, A - 1)
    print(len(Points))
    for i in Points:
        AddB(i)

# Function that randomly picks a rectangle(box) and place on location i
def AddB(i):
    global Box
    Box = random.choice(list(shapes.keys()))
    PlaceB(i)
    return None

# Function that replaces the outline of the rectangles with ascii art
def Outline():
    global MAP
    global b
    global LS
    global RS
    for i in MAP:
        if MAP[i] == "#":
            Sides = {"U": 0, "D": 0, "L": 0, "R": 0}
            # - U
            x = i - b
            try:
                a = MAP[x]
            except:
                a = " "
            if a == "~":
                Sides["U"] = 1
            # - U
            # - D
            x = i + b
            try:
                a = MAP[x]
            except:
                a = " "
            if a == "~":
                Sides["D"] = 1
            # - D
            # - L
            if i in LS:
                Sides["L"] = 0
            else:
                x = i - 1
                try:
                    a = MAP[x]
                except:
                    a = " "
                if a == "~":
                    Sides["L"] = 1
            # - L
            # - R
            if i in RS:
                Sides["R"] = 0
            else:
                x = i + 1
                try:
                    a = MAP[x]
                except:
                    a = " "
                if a == "~":
                    Sides["R"] = 1
            # - R
            if Sides["U"] == 1 and Sides["D"] == 1 and Sides["R"] == 1:
                MAP[i] = ">"  
            elif Sides["U"] == 1 and Sides["D"] == 1 and Sides["L"] == 1:   
                MAP[i] = "<"
            elif Sides["U"] == 1 and Sides["R"] == 1 and Sides["L"] == 1:   
                MAP[i] = "^"
            elif Sides["R"] == 1 and Sides["D"] == 1 and Sides["L"] == 1:   
                MAP[i] = "v"
            elif (Sides["U"] == 1 and Sides["L"] == 1) or (Sides["D"] == 1 and Sides["R"] == 1):
                MAP[i] = "/"
            elif (Sides["U"] == 1 and Sides["R"] == 1) or (Sides["D"] == 1 and Sides["L"] == 1):
                MAP[i] = u"\u005C"
            elif Sides["U"] == 1:
                MAP[i] = u"\u203E"
            elif Sides["D"] == 1:
                MAP[i] = "_"
            elif Sides["L"] == 1 or Sides["R"] == 1:
                MAP[i] = "|"
            else:
                pass

# Function that clears out overything but the sea and outline
def Clear():
    global MAP
    for i in MAP:
        if MAP[i] == "#":
            MAP[i] = symbols["river"]

# Function that adds random stuff to the empty parts of the map
def AddStuff():
    global MAP
    global PIL
    global stuff
    global p
    if p == "T":
        for i in MAP:
            if MAP[i] == " ":
                if random.randint(0, 25) == 1:
                    MAP[i] = random.choice(stuff)
                    if MAP[i] not in PIL:
                        PIL.append(MAP[i])
                    if MAP[i] == "@" or MAP[i] == "&" or MAP[i] == "+" or MAP[i] == "%" or MAP[i] == "#":
                        stuff.remove(MAP[i])

# Function that creats the Legend
def LegendC():
    global PIL
    global Legend
    global MAP
    global b
    Name = Namer()
    Hname = Hnamer()
    Dname = Dnamer()
    Meaning = {
    "^": "Land             |",
    "*": "Forest           |",
    "_": "Lake             |",
    " ": "River            |",
    "!": "City             |",
    "$": "Gold             |",
    "&": Dname,
    "@": Hname,
    "M": "Mountain         |",
    }
    Legend = {
        0: " +----------------------+",
        1: " |        " + Name + "        |",
        2: " +----------------------+"
    }
    n = 4
    for i in Meaning:
        Legend[n] = " | " + i + " = " + Meaning[i]
        n += 1
    Legend[a - 1] = " +----------------------+"

# Main loop
while True:
    print("Regenerate(1)")
    cmd = input(">")
    while cmd != "1":
        cmd = input(">")
    Start()
    DesignLocations()
    print("")
    Outline()
    Clear()
    AddStuff()
    LegendC()
    PrintM()
    print("")
