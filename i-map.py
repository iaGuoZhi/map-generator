import random
import os
import sys
import time

MAP_PARAMS = {
    "river_separate_param" : 30,
    "river_number" : 10,
    "river_number_random_param" : 3,
    "side_sea_number" : 2,
    "forest_rarity" : 6,
    "field_rarity" : 3,
    "mountain_rarity" : 25,
    "gold_rarity" : 10,
    "iron_rarity" : 18,
    "town_scope_param" : 1,
    "town_build_param" : 666,
    "state_number" : 10,
    "curve_corner_by_symbol_param" : 4,
    "curve_corner_by_color_param" : 6,
    "default_language" : "cn",
}

MAP_SYMBOLS = {
    "land": "^",
    "field": ".",
    "forest": "*",
    "water": " ",
    "town": "P",
    "gold" : "$",
    "iron" : "&",
    "mountain" : "M",
}

BOX_SIZE_LEVEL = {
    "sea": 10,
    "river": 1,
    "town": 2,
    "mountain": 8,
    "mineral": 5,
    "state": 40,
}

MAP_COLORS = {
    "blue": "\033[94m",
    "green": "\033[92m",
    "red": "\033[91m",
    "yellow": "\033[93m",
    "purple": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "reset": "\033[0m",
}

TOOL_SYMBOLS = {
    "illegal": "?",
}

global global_map_language
global_map_language = MAP_PARAMS["default_language"]

# Function that creates the basic map, defines stuff like size, legend, positions on left/right side, ect
def initialize_map():
    global global_map
    global global_color
    global globa_points
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
    global global_name

    global_map = {}
    global_color = {}
    global_points = []
    global_input_area_height = 3
    global_info_bar_width = 25
    size = os.get_terminal_size()
    global_height = size.lines - global_input_area_height
    global_width = size.columns - global_info_bar_width
    global_map_size = global_height * global_width
    for x in range(global_map_size):
        global_map[x] = MAP_SYMBOLS["land"]
        global_color[x] = MAP_COLORS["reset"]
    global_border = [x for x in range(global_map_size) if (x // global_width in (0, global_height - 1)) or (x % global_width == 0) or ((x + 1) % global_width == 0)]
    global_up_border = [x for x in range(global_map_size) if (x // global_width == 0)]
    global_down_border = [x for x in range(global_map_size) if (x // global_width == global_height - 1)]
    global_left_border = [x for x in range(global_map_size) if (x % global_width == 0)]
    global_right_border = [x for x in range(global_map_size) if ((x + 0) % global_width == 0)]
    global_border_group = [global_up_border, global_down_border, global_left_border, global_right_border]
    global_name = random_name()

# Functions that name stuff
def random_name():
    if global_map_language == "cn":
        fp = random.choice(["东","南","西","北", "前", "后"])
        sp = random.choice(["秦","楚","齐","燕", "赵", "魏", "韩", "汉", "吴", "蜀", "越", "宋", "晋", "唐", "明", "元"])
        return (fp + sp).center(16)
    elif global_map_language == "en":
        sp = random.choice(["Torrhen Stark","Ronnel Arryn","Harren Hoare","Loren I Lannister", "Mern IX Gardener", "Argilac Durrandon", "Meria Martell"])
        return sp.center(18)

# Function return symbol meaning according to current language
def get_symbol_meaning():
    if global_map_language == "cn":
        symbol_meaning = [
            "^ = 陆地".ljust(17),
            ". = 耕地".ljust(17),
            "* = 森林".ljust(17),
            "  = 水域".ljust(17),
            "M = 山脉".ljust(17),
            "$ = 金矿".ljust(17),
            "& = 铁矿".ljust(17),
            "P = 城镇".ljust(17),
        ]
    elif global_map_language == "en":
        symbol_meaning = [
            "^ = Land".ljust(19),
            ". = Field".ljust(19),
            "* = Forest".ljust(19),
            "  = Water".ljust(19),
            "M = Mountain".ljust(19),
            "$ = Gold".ljust(19),
            "& = Iron".ljust(19),
            "P = Town".ljust(19),
        ]
    else:
        symbol_meaning = {}

    return symbol_meaning

def get_map_statistics():
    water_area_size = 0
    land_area_size = 0
    population = 0
    gold_reserves = 0
    iron_reserves = 0

    for x in global_map:
        if global_map[x] == MAP_SYMBOLS["water"]:
            water_area_size += 1
        elif global_map[x] != MAP_SYMBOLS["water"]:
            land_area_size += 1
            if global_map[x] == MAP_SYMBOLS["town"]:
                population += 1
            elif global_map[x] == MAP_SYMBOLS["gold"]:
                gold_reserves += 1
            elif global_map[x] == MAP_SYMBOLS["iron"]:
                iron_reserves += 1
            else:
                pass
        else:
            pass

    if global_map_language == "cn":
        symbol_meaning = [
            ("陆地面积: %d" % land_area_size).ljust(15),
            ("水域面积: %d" % water_area_size).ljust(15),
            ("人口数量: %d" % population).ljust(15),
            ("金矿储备: %d" % gold_reserves).ljust(15),
            ("铁矿储备: %d" % iron_reserves).ljust(15),
        ]
    elif global_map_language == "en":
        symbol_meaning = [
            ("LAND AREA: %d" % land_area_size).ljust(19),
            ("WATER AREA: %d" % water_area_size).ljust(19),
            ("POPULATION: %d" % population).ljust(19),
            ("GOLD RESERVES: %d" % gold_reserves).ljust(19),
            ("IRON RESERVES: %d" % iron_reserves).ljust(19),
        ]
    else:
        symbol_meaning = []

    return symbol_meaning

# Function that creats the map introduction
def create_intro():
    global global_intro
    global_intro = {
        0: "   +--------------------+",
        1: "   | " + global_name + " |",
        2: "   +--------------------+"
    }
    n = 4
    # Print map statistics
    map_statistics = get_map_statistics()
    for i in map_statistics:
        global_intro[n] = "   | " + i + "|"
        n += 1

    # Print map symbol meaning
    n += 1
    symbol_meaning = get_symbol_meaning()
    for i in symbol_meaning:
        global_intro[n] = "   | " + i + "|"
        n += 1

    global_intro[global_height - 1] = "   +--------------------+"

def get_random_box(size_level):
    x = 1; y = 1
    for i in range(size_level):
        x += random.randint(0, 2)
        y += random.randint(0, 2)
    return {"x": x, "y": y}

# Function that places Box on x
def place_box(point, symbol):
    x = 0
    y = 0
    box = []
    while y != global_box["y"]:
        while x != global_box["x"]:
            if 0 <= point + y * global_width +x < global_map_size:
                box.append(point + y * global_width + x)
            x += 1
        y += 1
        x = 0
    for x in box:
        if global_map[x] == MAP_SYMBOLS["land"] or global_map[x] == MAP_SYMBOLS["field"] or global_map[x] == MAP_SYMBOLS["forest"]:
            global_map[x] = symbol

def place_color(point, color):
    x = 0
    y = 0
    box = []
    while y != global_box["y"]:
        while x != global_box["x"]:
            if 0 <= point + y * global_width +x < global_map_size:
                box.append(point + y * global_width + x)
            x += 1
        y += 1
        x = 0
    for x in box:
        global_color[x] = MAP_COLORS[color]

def pick_locations(begin, end):
   local_begin_row = begin // global_width
   local_begin_column = begin - local_begin_row * global_width
   local_end_row = end // global_width
   local_end_column = end - local_end_row * global_width

   if min(local_begin_row, local_end_row) + 1 >= max(local_begin_row, local_end_row) and min(local_begin_column, local_end_column) +1 >= max(local_begin_column, local_end_column):
       return
   # Randomly separate rivers
   if random.randint(0, MAP_PARAMS["river_separate_param"]) == 1:
       return

   local_mid_row = random.randint(min(local_begin_row, local_end_row), max(local_begin_row, local_end_row))
   local_mid_column = random.randint(min(local_begin_column, local_end_column), max(local_begin_column, local_end_column))
   local_mid = local_mid_row * global_width + local_mid_column
   if not local_mid in global_points:
       global_points.append(local_mid)
   pick_locations(begin, local_mid)
   pick_locations(local_mid, end)

def design_river_locations():
    global global_points
    global_points = []
    for local_i in range(MAP_PARAMS["river_number"] + MAP_PARAMS["river_number_random_param"]):
        point_a = random.choice(global_border)
        point_b = random.choice(global_border)
        global_points.append(point_a)
        global_points.append(point_b)
        pick_locations(point_a, point_b)
    return global_points

def design_sea_locations():
    global global_points
    global_points = []
    for local_i in range(MAP_PARAMS["side_sea_number"]):
        for x in range(4):
            point_a = random.choice(global_border_group[x])
            point_b = random.choice(global_border_group[x])
            global_points.append(point_a)
            global_points.append(point_b)
            pick_locations(point_a, point_b)
    return global_points

def design_normal_locations(rarity):
    global global_points
    global_points = []
    for local_i in global_map:
        if global_map[local_i] == MAP_SYMBOLS["land"]:
            if random.randint(0, rarity) == 1:
                global_points.append(local_i)
    return global_points

def design_state_locations():
    global global_points
    global_points = []
    for local_i in range(MAP_PARAMS["state_number"]):
        while True:
            point_a = random.randint(0, global_map_size - 1)
            if global_map[point_a] == MAP_SYMBOLS["town"]:
                global_points.append(point_a)
                break
    return global_points

def design_town_locations():
    points = []
    for local_i in global_map:
        town_suitability = 0
        for y in range(0 - MAP_PARAMS["town_scope_param"], MAP_PARAMS["town_scope_param"] + 1):
            for x in range(0 - MAP_PARAMS["town_scope_param"], MAP_PARAMS["town_scope_param"] + 1):
                side_point = local_i + y * global_width + x
                try:
                    side_symbol = global_map[side_point]
                except:
                    side_symbol = MAP_SYMBOLS["water"]

                if side_symbol == MAP_SYMBOLS["water"]:
                    town_suitability += random.randint(30, 130)
                elif side_symbol == MAP_SYMBOLS["gold"]:
                    town_suitability += random.randint(20, 160)
                elif side_symbol == MAP_SYMBOLS["iron"]:
                    town_suitability += random.randint(40, 130)
                elif side_symbol == MAP_SYMBOLS["mountain"]:
                    town_suitability += random.randint(20, 60)
                elif side_symbol == MAP_SYMBOLS["forest"]:
                    town_suitability += random.randint(20, 80)
                elif side_symbol == MAP_SYMBOLS["field"]:
                    town_suitability += random.randint(0, 120)
                else:
                    town_suitability += random.randint(0, 100)

        if town_suitability >= MAP_PARAMS["town_build_param"]:
            points.append(local_i)
    return points

# Function that smooths out long corners
def curve_corners_by_symbol(symbol):
    t = 0
    while t <= MAP_PARAMS["curve_corner_by_symbol_param"]:
        t += 1
        for i in global_map:
            if  global_map[i] == symbol:
                rectangle_sides = 0
                # - U
                x = i - global_width
                try:
                    up_symbol = global_map[x]
                except:
                    up_symbol = TOOL_SYMBOLS["illegal"]
                if up_symbol != symbol:
                    rectangle_sides += 1
                # - U
                # - D
                x = i + global_width
                try:
                    down_symbol = global_map[x]
                except:
                    down_symbol = TOOL_SYMBOLS["illegal"]
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
                        left_symbol = TOOL_SYMBOLS["illegal"]
                    if left_symbol != symbol:
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
                        right_symbol = TOOL_SYMBOLS["illegal"]
                    if right_symbol != symbol:
                        rectangle_sides += 1
                # -R
                if rectangle_sides == 4:
                    global_map[i] = MAP_SYMBOLS["land"]
                elif rectangle_sides == 1 and t <= MAP_PARAMS["curve_corner_by_symbol_param"]:
                    if random.randint(0, 50) == 1:
                        global_map[i] = MAP_SYMBOLS["land"]
                elif rectangle_sides == 2 and t <= MAP_PARAMS["curve_corner_by_symbol_param"]:
                    if random.randint(0, 3) != 1:
                        global_map[i] = MAP_SYMBOLS["land"]
                elif rectangle_sides == 3 and t <= MAP_PARAMS["curve_corner_by_symbol_param"]:
                    if random.randint(0, 5) != 1:
                        global_map[i] = MAP_SYMBOLS["land"]
                else:
                    pass

def curve_corners_by_color(color):
    t = 0
    while t <= MAP_PARAMS["curve_corner_by_color_param"]:
        t += 1
        for i in global_map:
            if  global_color[i] == MAP_COLORS[color]:
                rectangle_sides = 0
                # - U
                x = i - global_width
                try:
                    up_symbol = global_color[x]
                except:
                    up_symbol = TOOL_SYMBOLS["illegal"]
                if up_symbol != MAP_COLORS[color]:
                    rectangle_sides += 1
                # - U
                # - D
                x = i + global_width
                try:
                    down_symbol = global_color[x]
                except:
                    down_symbol = TOOL_SYMBOLS["illegal"]
                if down_symbol != MAP_COLORS[color]:
                    rectangle_sides += 1
                # - D
                # - L
                if i in global_left_border:
                    pass
                else:
                    x = i - 1
                    try:
                        left_symbol = global_color[x]
                    except:
                        left_symbol = TOOL_SYMBOLS["illegal"]
                    if left_symbol != MAP_COLORS[color]:
                        rectangle_sides += 1
                # - L
                # - R
                if i + 1 in global_right_border:
                    pass
                else:
                    x = i + 1
                    try:
                        right_symbol = global_color[x]
                    except:
                        right_symbol = TOOL_SYMBOLS["illegal"]
                    if right_symbol != MAP_COLORS[color]:
                        rectangle_sides += 1
                # -R
                if rectangle_sides == 4:
                    global_color[i] = MAP_COLORS["reset"]
                elif rectangle_sides == 1 and t <= MAP_PARAMS["curve_corner_by_color_param"]:
                    if random.randint(0, 50) == 1:
                        global_color[i] = MAP_COLORS["reset"]
                elif rectangle_sides == 2 and t <= MAP_PARAMS["curve_corner_by_color_param"]:
                    if random.randint(0, 3) != 1:
                        global_color[i] = MAP_COLORS["reset"]
                elif rectangle_sides == 3 and t <= MAP_PARAMS["curve_corner_by_color_param"]:
                    if random.randint(0, 5) != 1:
                        global_color[i] = MAP_COLORS["reset"]
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
                up_symbol = TOOL_SYMBOLS["illegal"]
            if up_symbol == MAP_SYMBOLS["land"]:
                rectangle_sides["U"] = 1
            # - U
            # - D
            x = i + global_width
            try:
                down_symbol = global_map[x]
            except:
                down_symbol = TOOL_SYMBOLS["illegal"]
            if down_symbol == MAP_SYMBOLS["land"]:
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
                    left_symbol = TOOL_SYMBOLS["illegal"]
                if left_symbol == MAP_SYMBOLS["land"]:
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
                    right_symbol = TOOL_SYMBOLS["illegal"]
                if right_symbol == MAP_SYMBOLS["land"]:
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
    outline_border(MAP_SYMBOLS["water"])

def build_river():
    global global_box
    points = design_river_locations()
    points.sort()
    for x in points:
        global_box = get_random_box(BOX_SIZE_LEVEL["river"])
        place_box(x, MAP_SYMBOLS["water"])

def build_sea():
    global global_box
    points = design_sea_locations()
    points.sort()
    for x in points:
        global_box = get_random_box(BOX_SIZE_LEVEL["sea"])
        place_box(x, MAP_SYMBOLS["water"])

def build_forest():
    points = design_normal_locations(MAP_PARAMS["forest_rarity"])
    for x in points:
        global_map[x] = MAP_SYMBOLS["forest"]

def build_field():
    points = design_normal_locations(MAP_PARAMS["field_rarity"])
    for x in points:
        global_map[x] = MAP_SYMBOLS["field"]

def build_mountains():
    global global_box
    points = design_normal_locations(MAP_PARAMS["mountain_rarity"])
    for x in points:
        global_box = get_random_box(BOX_SIZE_LEVEL["mountain"])
        place_box(x, MAP_SYMBOLS["mountain"])
    curve_corners_by_symbol(MAP_SYMBOLS["mountain"])

def build_mineral():
    global global_box
    points = design_normal_locations(MAP_PARAMS["gold_rarity"])
    for x in points:
        global_box = get_random_box(BOX_SIZE_LEVEL["mineral"])
        place_box(x, MAP_SYMBOLS["gold"])
    curve_corners_by_symbol(MAP_SYMBOLS["gold"])

    points = design_normal_locations(MAP_PARAMS["iron_rarity"])
    for x in points:
        global_box = get_random_box(BOX_SIZE_LEVEL["mineral"])
        place_box(x, MAP_SYMBOLS["iron"])
    curve_corners_by_symbol(MAP_SYMBOLS["iron"])

def build_towns():
    global global_box
    points = design_town_locations()
    points.sort()
    for x in points:
        global_box = get_random_box(BOX_SIZE_LEVEL["town"])
        place_box(x, MAP_SYMBOLS["town"])

def build_state():
    global global_box
    points = design_state_locations()
    for x in points:
        global_box = get_random_box(BOX_SIZE_LEVEL["state"])
        color = random.choice(list(MAP_COLORS.keys())[:len(MAP_COLORS) - 1])
        place_color(x, color)
    for color in MAP_COLORS.keys():
        if color != "reset":
            curve_corners_by_color(color)

def user_input():
    global global_map_language
    print("Regenerate(1) Set map language(2)")
    cmd = input(">")
    while cmd != "1":
        if cmd == "2":
            print("Input language: Chinese(cn), English(en)")
            language = input(">")
            print(language)
            if language == "cn":
                global_map_language = "cn"
            elif language == "en":
                global_map_language = "en"
            else:
                pass

        print("Regenerate(1) Set map language(2)")
        cmd = input(">")

# Function that prints the map to the console
def print_map():
    c = 0
    x = 0
    i = 0
    for i in range(global_height):
        for x in range(global_width):
            print(f"{global_color[c]}{global_map[c]}{MAP_COLORS['reset']}", end = "")
            x += 1
            c += 1
        try:
            print(global_intro[i])
        except:
            print("   |                    |")
        x = 1
        i += 1

def save_map():
    timestamp = time.strftime("%Y-%m-%dT%H:%M%SZ")
    file_name = "output/" + global_name.strip() + "_" + timestamp + ".txt"
    original_stdout = sys.stdout
    with open(file_name, 'w') as output_file:
        sys.stdout = output_file
        print_map()
        sys.stdout = original_stdout

# Main loop
while True:
    user_input()
    initialize_map()
    build_water()
    build_mountains()
    build_mineral()
    build_forest()
    build_field()
    build_towns()
    build_state()
    create_intro()
    print_map()
    save_map()
    print("")
