import random
import os

# - Lists of rectangles
SEA_BOX_SHAPES_1 = {
    1:{"x": 5, "y": 5},
    2:{"x": 7, "y": 4},
    3:{"x": 8, "y": 5},
    4:{"x": 6, "y": 7},
    5:{"x": 5, "y": 9},
}

RIVER_BOX_SHAPES_1 = {
    1:{"x": 3, "y": 4},
    2:{"x": 4, "y": 3},
    3:{"x": 4, "y": 2},
    4:{"x": 3, "y": 3},
}

TOWN_BOX_SHAPES_1 = {
    1:{"x": 3, "y": 3},
    2:{"x": 4, "y": 4},
    3:{"x": 2, "y": 2},
    4:{"x": 1, "y": 2},
    5:{"x": 2, "y": 2},
    6:{"x": 1, "y": 2},
}

MOUNTAIN_BOX_SHAPES_1 = {
    1:{"x": 5, "y": 5},
    2:{"x": 4, "y": 7},
    3:{"x": 8, "y": 9},
    4:{"x": 5, "y": 6},
}

MINERAL_BOX_SHAPES_1 = {
    1:{"x": 7, "y": 5},
    2:{"x": 3, "y": 5},
    3:{"x": 9, "y": 8},
    4:{"x": 5, "y": 6},
}

GLOBAL_MAP_SYMBOLS = {
    "land": "^",
    "forest": "*",
    "lake": "_",
    "river": " ",
    "sea": " ",
    "town": "P",
    "gold" : "$",
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
    global global_up_border
    global global_down_border
    global global_left_border
    global global_right_border
    global global_border_group
    global global_border
    global global_input_area_height
    global global_info_bar_width
    global global_curve_corner_param
    global global_map_language

    global_map = {}
    global_input_area_height = 3
    global_info_bar_width = 25
    global_curve_corner_param = 5
    global_map_language = "cn"
    size = os.get_terminal_size()
    global_height = size.lines - global_input_area_height
    global_width = size.columns - global_info_bar_width
    global_map_size = global_height * global_width
    for x in range(global_map_size):
        global_map[x] = GLOBAL_MAP_SYMBOLS["land"]
    global_border = [x for x in range(global_map_size) if (x // global_width in (0, global_height - 1)) or (x % global_width == 0) or ((x + 1) % global_width == 0)]
    global_up_border = [x for x in range(global_map_size) if (x // global_width == 0)]
    global_down_border = [x for x in range(global_map_size) if (x // global_width == global_height - 1)]
    global_left_border = [x for x in range(global_map_size) if (x % global_width == 0)]
    global_right_border = [x for x in range(global_map_size) if ((x + 0) % global_width == 0)]
    global_border_group = [global_up_border, global_down_border, global_left_border, global_right_border]

# Functions that name stuff
def random_name():
    if global_map_language == "cn":
        FP = random.choice(["东","南","西","北", "前", "后"])
        SP = random.choice(["秦","楚","齐","燕", "赵", "魏", "韩", "汉", "吴", "蜀", "越", "宋", "晋", "唐", "明", "元"])
        return FP + SP

# Function return symbol meaning according to current language
def get_symbol_meaning():
    if global_map_language == "cn":
        symbol_meaning = {
            "^": "陆地             |",
            "*": "森林             |",
            " ": "水域             |",
            "M": "山脉             |",
            "$": "金矿             |",
            "P": "城镇             |",
        }
    elif global_map_language == "en":
        symbol_meaning = {
            "^": "Land             |",
            "*": "Forest           |",
            " ": "Water            |",
            "M": "Mountain         |",
            "$": "Gold             |",
            "P": "Town             |",
        }
    else:
        symbol_meaning = {}

    return symbol_meaning

# Function that creats the map introduction
def create_intro():
    global global_intro
    name = random_name()
    global_intro = {
        0: " +----------------------+",
        1: " |         " + name + "         |",
        2: " +----------------------+"
    }
    n = 4
    # Print map symbol meaning
    symbol_meaning = get_symbol_meaning()
    for i in symbol_meaning:
        global_intro[n] = " | " + i + " = " + symbol_meaning[i]
        n += 1

    global_intro[global_height - 1] = " +----------------------+"

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
            print(global_intro[i])
        except:
            print(" |                      |")
        x = 1
        i += 1

# Function that places Box on x
def place_box(point, symbol):
    box = [x for x in range(global_map_size) if ((0 <= (x // global_width) - (point // global_width) < global_shapes[global_box]["y"]) and (0 <= (x % global_width) - (point % global_width) < global_shapes[global_box]["x"]))]
    for x in box:
        if global_map[x] == GLOBAL_MAP_SYMBOLS["land"] or global_map[x] == GLOBAL_MAP_SYMBOLS["forest"]:
            global_map[x] = symbol

def pick_locations(begin, end):
   local_begin_row = begin // global_width
   local_begin_column = begin - local_begin_row * global_width
   local_end_row = end // global_width
   local_end_column = end - local_end_row * global_width

   if min(local_begin_row, local_end_row) + 1 >= max(local_begin_row, local_end_row) and min(local_begin_column, local_end_column) +1 >= max(local_begin_column, local_end_column):
       return
   # Randomly separate rivers
   if random.randint(0, 30) == 1:
       return

   local_mid_row = random.randint(min(local_begin_row, local_end_row), max(local_begin_row, local_end_row))
   local_mid_column = random.randint(min(local_begin_column, local_end_column), max(local_begin_column, local_end_column))
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
        for local_i in range(7):
            point_a = random.choice(global_border)
            point_b = random.choice(global_border)
            global_points.append(point_a)
            global_points.append(point_b)
            pick_locations(point_a, point_b)
        return global_points
    elif geo_type == "sea":
        for local_i in range(2):
            # Actually, only left and up border and build sea, as box is built towards right and down orientation
            for x in range(4):
                point_a = random.choice(global_border_group[x])
                point_b = random.choice(global_border_group[x])
                global_points.append(point_a)
                global_points.append(point_b)
                pick_locations(point_a, point_b)
        return global_points
    elif geo_type == "forest":
        for local_i in global_map:
            if global_map[local_i] == GLOBAL_MAP_SYMBOLS["land"]:
                if random.randint(0, 5) == 1:
                    global_points.append(local_i)
        return global_points
    # Town should built near water, mineral
    elif geo_type == "town":
        for local_i in global_map:
            town_suitability = 0
            for x in range(3):
                for y in range(3):
                    try:
                        side_symbol = global_map[local_i + y * global_width + x]
                    except:
                        side_symbol = GLOBAL_MAP_SYMBOLS["sea"]

                    if side_symbol == GLOBAL_MAP_SYMBOLS["river"] or side_symbol == GLOBAL_MAP_SYMBOLS["sea"]:
                        town_suitability += random.randint(30, 130)
                    elif side_symbol == GLOBAL_MAP_SYMBOLS["gold"]:
                        town_suitability += random.randint(20, 150)
                    elif side_symbol == GLOBAL_MAP_SYMBOLS["mountain"]:
                        town_suitability += random.randint(20, 60)
                    else:
                        town_suitability += random.randint(0, 100)

            if town_suitability >= 660:
                global_points.append(local_i)
        return global_points
    elif geo_type == "mountain":
        for local_i in range(20):
            point_a = random.randint(0, global_map_size - 1)
            global_points.append(point_a)
        return global_points
    elif geo_type == "gold":
        for local_i in range(10):
            point_a = random.randint(0, global_map_size - 1)
            global_points.append(point_a)
        return global_points
    else:
        return None

# Function that smooths out long corners
def curve_corners(symbol):
    t = 0
    while t <= global_curve_corner_param:
        t += 1
        for i in global_map:
            if  global_map[i] == symbol:
                rectangle_sides = 0
                # - U
                x = i - global_width
                try:
                    up_symbol = global_map[x]
                except:
                    up_symbol = GLOBAL_TOOL_SYMBOLS["illegal"]
                if up_symbol != symbol:
                    rectangle_sides += 1
                # - U
                # - D
                x = i + global_width
                try:
                    down_symbol = global_map[x]
                except:
                    down_symbol = GLOBAL_TOOL_SYMBOLS["illegal"]
                if down_symbol != symbol:
                    rectangle_sides += 1
                # - D
                # - L
                if i in global_left_border:
                    pass
                else:
                    x = i - 1
                    try:
                        left_symbol = global_map[x]
                    except:
                        left_symbol = GLOBAL_TOOL_SYMBOLS["illegal"]
                    if down_symbol != symbol:
                        rectangle_sides += 1
                # - L
                # - R
                if i + 1 in global_right_border:
                    pass
                else:
                    x = i + 1
                    try:
                        right_symbol = global_map[x]
                    except:
                        right_symbol = GLOBAL_TOOL_SYMBOLS["illegal"]
                    if down_symbol != symbol:
                        rectangle_sides += 1
                # -R
                if rectangle_sides == 4:
                    global_map[i] = GLOBAL_MAP_SYMBOLS["land"]
                elif rectangle_sides == 1 and t <= global_curve_corner_param:
                    if random.randint(0, 50) == 1:
                        global_map[i] = GLOBAL_MAP_SYMBOLS["land"]
                elif rectangle_sides == 2 and t <= global_curve_corner_param:
                    if random.randint(0, 3) != 1:
                        global_map[i] = GLOBAL_MAP_SYMBOLS["land"]
                elif rectangle_sides == 3 and t <= global_curve_corner_param:
                    if random.randint(0, 5) != 1:
                        global_map[i] = GLOBAL_MAP_SYMBOLS["land"]
                else:
                    pass

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

def build_water():
    build_sea()
    build_river()
    outline_border(GLOBAL_MAP_SYMBOLS["river"])

def build_river():
    global global_box
    global global_shapes
    global_shapes = RIVER_BOX_SHAPES_1
    points = design_locations("river")
    for x in points:
        global_box = random.choice(list(global_shapes.keys()))
        place_box(x, GLOBAL_MAP_SYMBOLS["river"])

def build_sea():
    global global_box
    global global_shapes
    global_shapes = SEA_BOX_SHAPES_1
    points = design_locations("sea")
    for x in points:
        global_box = random.choice(list(global_shapes.keys()))
        place_box(x, GLOBAL_MAP_SYMBOLS["sea"])

def build_forest():
    global global_box
    points = design_locations("forest")
    for x in points:
        global_map[x] = GLOBAL_MAP_SYMBOLS["forest"]

def build_towns():
    global global_box
    global global_shapes
    global_shapes = TOWN_BOX_SHAPES_1
    points = design_locations("town")
    for x in points:
        global_box = random.choice(list(global_shapes.keys()))
        place_box(x, GLOBAL_MAP_SYMBOLS["town"])

def build_mountains():
    global global_box
    global global_shapes
    global_shapes = MOUNTAIN_BOX_SHAPES_1
    points = design_locations("mountain")
    for x in points:
        global_box = random.choice(list(global_shapes.keys()))
        place_box(x, GLOBAL_MAP_SYMBOLS["mountain"])
    curve_corners(GLOBAL_MAP_SYMBOLS["mountain"])

def build_mineral():
    global global_box
    global global_shapes
    global_shapes = MINERAL_BOX_SHAPES_1
    points = design_locations("gold")
    for x in points:
        global_box = random.choice(list(global_shapes.keys()))
        place_box(x, GLOBAL_MAP_SYMBOLS["gold"])
    curve_corners(GLOBAL_MAP_SYMBOLS["gold"])

# Main loop
while True:
    print("Regenerate(1)")
    cmd = input(">")
    while cmd != "1":
        cmd = input(">")
    initialize_map()
    build_water()
    build_mountains()
    build_mineral()
    build_forest()
    build_towns()
    create_intro()
    print_map()
    print("")
