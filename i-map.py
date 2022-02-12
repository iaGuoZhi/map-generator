# - i-map

import random
import os

# - Lists of rectangles
GLOBAL_SHAPES_1 = {
    1:{"x": 4, "y": 4},
}

GLOBAL_MAP_SYMBOLS = {
    "land": "^",
    "forest": "*",
    "lake": "_",
    "river": " ",
    "town": "!",
    "gold" : "@",
    "mountain" : "M",
}

GLOBAL_TOOL_SYMBOLS = {
    "illegal": "?",
}

# Function that creates the basic map, defines stuff like size, legend, positions on left/right side, ect
def initialize_map():
    global global_map
    global global_shapes
    global global_height
    global global_width
    global global_map_size
    global global_left_border
    global global_right_border
    global global_border
    global global_input_area_height
    global global_info_bar_width

    global_map = {}
    global_shapes = GLOBAL_SHAPES_1
    global_input_area_height = 3
    global_info_bar_width = 25
    size = os.get_terminal_size()
    global_height = size.lines - global_input_area_height
    global_width = size.columns - global_info_bar_width
    global_map_size = global_height * global_width
    for x in range(global_map_size):
        global_map[x] = GLOBAL_MAP_SYMBOLS["land"]
    global_border = [x for x in range(global_map_size) if (x // global_width in (0, global_height - 1)) or (x % global_width == 0) or ((x + 1) % global_width == 0)]
    global_left_border = [x for x in range(global_map_size) if (x % global_width == 0)]
    global_right_border = [x for x in range(global_map_size) if ((x + 0) % global_width == 0)]

# Functions that name stuff
def random_name():
    FP = random.choice(["东","南","西","北", "前", "后", "江"])
    SP = random.choice(["秦","楚","齐","燕", "赵", "魏", "韩", "汉", "吴", "越", "宋", "晋", "唐", "明", "元"])
    return FP + SP

# Function that prints the map to the console
def print_map():
    c = 0
    x = 0
    i = 0
    for i in range(global_height):
        for x in range(global_width):
            print(global_map[c], end = "")
            x += 1
            c += 1
        try:
            print(Legend[i])
        except:
            print(" |                      |")
        x = 1
        i += 1

# Function that places Box on x
def place_box(point, symbol):
    box = [x for x in range(global_map_size) if ((0 <= (x // global_width) - (point // global_width) < global_shapes[global_box]["y"]) and (0 <= (x % global_width) - (point % global_width) < global_shapes[global_box]["x"]))]
    for x in box:
        global_map[x] = symbol

def pick_locations(begin, end):
   local_begin_row = begin // global_width
   local_begin_column = begin - local_begin_row * global_width
   local_end_row = end // global_width
   local_end_column = end - local_end_row * global_width

   local_mid_row = random.randint(min(local_begin_row, local_end_row), max(local_begin_row, local_end_row))
   local_mid_column = random.randint(min(local_begin_column, local_end_column), max(local_begin_column, local_end_column))
   if ((local_mid_row == min(local_begin_row, local_end_row)) and (local_mid_column == min(local_begin_column, local_end_column))):
       return
   else:
       local_mid = local_mid_row * global_width + local_mid_column
       if not local_mid in global_points:
           global_points.append(local_mid)
       pick_locations(begin, local_mid)
       pick_locations(local_mid, end)

# Function that design which locations to place box
def design_locations(geo_type):
    global global_points
    global_points = []
    local_i = 0
    if geo_type == "river":
        for local_i in range(6):
            point_a = random.choice(global_border)
            point_b = random.choice(global_border)
            print(point_a // global_width, point_a % global_width)
            print(point_b // global_width, point_b % global_width)
            global_points.append(point_a)
            global_points.append(point_b)
            pick_locations(point_a, point_b)
        return global_points
    elif geo_type == "forest":
        for local_i in range(20):
            point_a = random.randint(0, global_map_size - 1)
            global_points.append(point_a)
        return global_points
    elif geo_type == "town":
        for local_i in range(20):
            point_a = random.randint(0, global_map_size - 1)
            global_points.append(point_a)
        return global_points
    elif geo_type == "mountain":
        for local_i in range(5):
            point_a = random.randint(0, global_map_size - 1)
            global_points.append(point_a)
        return global_points
    elif geo_type == "gold":
        for local_i in range(5):
            point_a = random.randint(0, global_map_size - 1)
            global_points.append(point_a)
        return global_points
    else:
        return None

# Function that replaces the outline of the rectangles with ascii art
def outline_border(symbol):
    for i in global_map:
        if global_map[i] == symbol:
            rectangle_sides = {"U": 0, "D": 0, "L": 0, "R": 0}
            # - U
            x = i - global_width
            try:
                up_symbol = global_map[x]
            except:
                up_symbol = GLOBAL_TOOL_SYMBOLS["illegal"]
            if up_symbol == GLOBAL_MAP_SYMBOLS["land"]:
                rectangle_sides["U"] = 1
            # - U
            # - D
            x = i + global_width
            try:
                down_symbol = global_map[x]
            except:
                down_symbol = GLOBAL_TOOL_SYMBOLS["illegal"]
            if down_symbol == GLOBAL_MAP_SYMBOLS["land"]:
                rectangle_sides["D"] = 1
            # - D
            # - L
            if i in global_left_border:
                rectangle_sides["L"] = 0
            else:
                x = i - 1
                try:
                    left_symbol = global_map[x]
                except:
                    left_symbol = GLOBAL_TOOL_SYMBOLS["illegal"]
                if left_symbol == GLOBAL_MAP_SYMBOLS["land"]:
                    rectangle_sides["L"] = 1
            # - L
            # - R
            if i + 1 in global_right_border:
                rectangle_sides["R"] = 0
            else:
                x = i + 1
                try:
                    right_symbol = global_map[x]
                except:
                    right_symbol = GLOBAL_TOOL_SYMBOLS["illegal"]
                if right_symbol == GLOBAL_MAP_SYMBOLS["land"]:
                    rectangle_sides["R"] = 1
            # - R
            if rectangle_sides["U"] == 1 and rectangle_sides["D"] == 1 and rectangle_sides["R"] == 1:
                global_map[i] = ">"  
            elif rectangle_sides["U"] == 1 and rectangle_sides["D"] == 1 and rectangle_sides["L"] == 1:   
                global_map[i] = "<"
            elif rectangle_sides["U"] == 1 and rectangle_sides["R"] == 1 and rectangle_sides["L"] == 1:   
                global_map[i] = "^"
            elif rectangle_sides["R"] == 1 and rectangle_sides["D"] == 1 and rectangle_sides["L"] == 1:   
                global_map[i] = "v"
            elif (rectangle_sides["U"] == 1 and rectangle_sides["L"] == 1) or (rectangle_sides["D"] == 1 and rectangle_sides["R"] == 1):
                global_map[i] = "/"
            elif (rectangle_sides["U"] == 1 and rectangle_sides["R"] == 1) or (rectangle_sides["D"] == 1 and rectangle_sides["L"] == 1):
                global_map[i] = u"\u005C"
            elif rectangle_sides["U"] == 1:
                global_map[i] = u"\u203E"
            elif rectangle_sides["D"] == 1:
                global_map[i] = "_"
            elif rectangle_sides["L"] == 1 or rectangle_sides["R"] == 1:
                global_map[i] = "|"
            else:
                pass

def build_river():
    global global_box
    points = design_locations("river")
    for x in points:
        global_box = random.choice(list(global_shapes.keys()))
        place_box(x, GLOBAL_MAP_SYMBOLS["river"])
    outline_border(GLOBAL_MAP_SYMBOLS["river"])

def build_forest():
    global global_box
    points = design_locations("forest")
    for x in points:
        global_box = random.choice(list(global_shapes.keys()))
        place_box(x, GLOBAL_MAP_SYMBOLS["forest"])

def build_towns():
    global global_box
    points = design_locations("town")
    for x in points:
        global_box = random.choice(list(global_shapes.keys()))
        place_box(x, GLOBAL_MAP_SYMBOLS["town"])

def build_mountains():
    global global_box
    points = design_locations("mountain")
    for x in points:
        global_box = random.choice(list(global_shapes.keys()))
        place_box(x, GLOBAL_MAP_SYMBOLS["mountain"])

def build_mineral():
    global global_box
    points = design_locations("gold")
    for x in points:
        global_box = random.choice(list(global_shapes.keys()))
        place_box(x, GLOBAL_MAP_SYMBOLS["gold"])

# Main loop
while True:
    print("Regenerate(1)")
    cmd = input(">")
    while cmd != "1":
        cmd = input(">")
    initialize_map()
    build_river()
    build_forest()
    build_towns()
    build_mountains()
    build_mineral()
    print("")
    print_map()
    print("")
