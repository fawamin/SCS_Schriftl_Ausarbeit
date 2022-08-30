import pygame
import pygame_menu



#User Changeable Variables
######################################################################################

#Defines Window Size on Startup
WINDOW_SIZE = {
    "WGA":(854, 480),
    "HD": (1280, 720),
    "FHD": (1920, 1080),
    "UWFHD": (2560, 1080),
    "WQHD": (2560, 1440),
    "UWQHD": (3440, 1440),
    "UHD": (3840, 2160),
    "custom": (1600, 900),
}["custom"]

#FPS Setting
FPS = 60

#Save Directory location relative to Main Folder
DIR_SAVE = "./Saves/"


#Default Values for Game Creation
DEFAULT_ROWS = 30
DEFAULT_COLS = 30
DEFAULT_INFINITY_PLAY_AREA = False
DEFAULT_CELL_SIZE = 15
DEFAULT_CELL_MARGIN = 2
DEFAULT_CELL_BORDER_RADIUS = 2
DEFAULT_CELL_HOVER_BORDER_WIDTH = 2


#Patterns for Playing 
PATTERNS = {
    # "description": list (rows)[list (columns)[cell state (int | None), < 0 | None = ignord, 0 kill cell, > 0 = born cell>]]
    "block": [[1, 1], [1, 1]],
    "beehive": [[1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1]],
    "leaf": [[0, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]],
    "boat": [[0, 1, 0], [1, 0, 1], [0, 1, 1]],
    "tub": [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
    "blinker": [[1, 1, 1]],
    "toad": [[0, 1, 1, 1], [1, 1, 1, 0]],
    "beacon": [[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 1]],
    "pulsar": [
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1], 
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0], 
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]
        ],
    "glider": [[0, 1, 0], [0, 0, 1], [1, 1, 1]],
    "LWSS": [[1, 0, 0, 1, 0], [0, 0, 0, 0, 1], [1, 0, 0, 0, 1], [0, 1, 1, 1, 1]],
    "MWSS": [[0, 0, 1, 0, 0, 0], [1, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1], [0, 1, 1, 1, 1, 1]],
    "HWSS": [[0, 0, 1, 1, 0, 0, 0], [1, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1], [0, 1, 1, 1, 1, 1, 1]],
    "snake": [[1, 0, 1, 1], [1, 1, 0, 1]],
    "ship": [[1, 1, 0], [1, 0, 1], [0, 1, 1]],
    "aircraft": [[1, 1, 0, 0], [1, 0, 0, 1], [0, 0, 1, 1]],
    "barge": [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]],
    "python": [[0, 0, 0, 1, 1], [1, 0, 1, 0, 1], [1, 1, 0, 0, 0]],
    "long boat": [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 1]],
}

#Don't Change Below
######################################################################################

#Titles for Menus
TITLE_BASE = "GameOfLife"
TITLE_MAIN_MENU = "Main Menu"
TITLE_ABOUT = "About"
TITLE_FROMSETTINGS = "New Game"
TITLE_FROMFILE = "Load File"

#Valid integer for User unput
VALIDINTCHARS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

#About Section
ABOUT = [
    f'Game of Life is a cellular automaton devised by the British mathematician John Horton Conway in 1970.',
    f'The game is a zero-player game, meaning that its evolution is determined by its initial state,',
    f'which is created by dead or alive cells. The game is self-similar, with the grid of cells',
    f'evolving over time according to the following rules:',
    f'1. Any live cell with fewer than two live neighbours dies, as if caused by under-population.',
    f'2. Any live cell with two or three live neighbours lives on to the next generation.',
    f'3. Any live cell with more than three live neighbours dies, as if by over-population.',
    f'4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.',
    f'',
    f'How to Play:',
    f'1. Start a new game or load a saved game.',
    f'2. Toggel a cell between alive and dead state or place a pattern.',
    f'3. Start the Day Cycle.',
    f'4. Save the current game.',
    f'',
    f'Controls:',
    f'Selection Type: single',
    f'Left Click - Toggle a cell between alive and dead state.',
    f'Right Click - Kill Cell.',
    f'',
    f'Selection Type: pattern',
    f'Left Click - Place a pattern.',
    f'Left Click + Ctrl - Place a pattern and don\'t kill cells.',
    f'Right Click - place a pattern invertet.',
    f'Right Click + Ctrl - place a pattern invertet and don\'t birth cells.',
    f'',
    f'Author: Steffen Hill, Fabian Waltermann',
    f'Pygame {pygame.__version__}',
    f'pygame-menu {pygame_menu.__version__}',
    ]

FONT_SIZE = 20

DAY_CYCLE_SPEEDS = {
    # "description": milliseconds between each day
    "5 s/d": 5000,
    "4 s/d": 4000,
    "3 s/d": 3000,
    "2 s/d": 2000,
    "1 d/s": 1000,
    "2 d/s": 500,
    "4 d/s": 250,
    "8 d/s": 125,
}

# Colour value for Cell Generations
COLOR_CELL = {
    0: {"STATE": "DEAD", "MIN_DAYS": 0, "COLOR": (0, 0, 0)},
    1: {"STATE": "GEN_1", "MIN_DAYS": 1, "COLOR": (255, 255, 255)},
    2: {"STATE": "GEN_2", "MIN_DAYS": 10, "COLOR": (223, 223, 255)},
    3: {"STATE": "GEN_3", "MIN_DAYS": 20, "COLOR": (191, 191, 255)},
    4: {"STATE": "GEN_4", "MIN_DAYS": 30, "COLOR": (159, 159, 255)},
    5: {"STATE": "GEN_5", "MIN_DAYS": 40, "COLOR": (127, 127, 255)},
    6: {"STATE": "GEN_6", "MIN_DAYS": 50, "COLOR": (95, 95, 255)},
    7: {"STATE": "GEN_7", "MIN_DAYS": 60, "COLOR": (63, 63, 255)},
    8: {"STATE": "GEN_8", "MIN_DAYS": 70, "COLOR": (31, 31, 255)},
    9: {"STATE": "GEN_9", "MIN_DAYS": 80, "COLOR": (0, 0, 255)},
    10: {"STATE": "GEN_10", "MIN_DAYS": 90, "COLOR": (0, 31, 255)},
    11: {"STATE": "GEN_11", "MIN_DAYS": 100, "COLOR": (0, 63, 255)},
    12: {"STATE": "GEN_12", "MIN_DAYS": 110, "COLOR": (0, 95, 255)},
    13: {"STATE": "GEN_13", "MIN_DAYS": 120, "COLOR": (0, 127, 255)},
    14: {"STATE": "GEN_14", "MIN_DAYS": 130, "COLOR": (0, 159, 255)},
    15: {"STATE": "GEN_15", "MIN_DAYS": 140, "COLOR": (0, 191, 255)},
    16: {"STATE": "GEN_16", "MIN_DAYS": 150, "COLOR": (0, 223, 255)},
    17: {"STATE": "GEN_17", "MIN_DAYS": 160, "COLOR": (0, 255, 255)},
    18: {"STATE": "GEN_18", "MIN_DAYS": 170, "COLOR": (0, 255, 223)},
    19: {"STATE": "GEN_19", "MIN_DAYS": 180, "COLOR": (0, 255, 191)},
    20: {"STATE": "GEN_20", "MIN_DAYS": 190, "COLOR": (0, 255, 159)},
    21: {"STATE": "GEN_21", "MIN_DAYS": 200, "COLOR": (0, 255, 127)},
    22: {"STATE": "GEN_22", "MIN_DAYS": 210, "COLOR": (0, 255, 95)},
    23: {"STATE": "GEN_23", "MIN_DAYS": 220, "COLOR": (0, 255, 63)},
    24: {"STATE": "GEN_24", "MIN_DAYS": 230, "COLOR": (0, 255, 31)},
    25: {"STATE": "GEN_25", "MIN_DAYS": 240, "COLOR": (0, 255, 0)},
    26: {"STATE": "GEN_26", "MIN_DAYS": 250, "COLOR": (31, 255, 0)},
    27: {"STATE": "GEN_27", "MIN_DAYS": 260, "COLOR": (63, 255, 0)},
    28: {"STATE": "GEN_28", "MIN_DAYS": 270, "COLOR": (95, 255, 0)},
    29: {"STATE": "GEN_29", "MIN_DAYS": 280, "COLOR": (127, 255, 0)},
    30: {"STATE": "GEN_30", "MIN_DAYS": 290, "COLOR": (159, 255, 0)},
    31: {"STATE": "GEN_31", "MIN_DAYS": 300, "COLOR": (191, 255, 0)},
    32: {"STATE": "GEN_32", "MIN_DAYS": 310, "COLOR": (223, 255, 0)},
    33: {"STATE": "GEN_33", "MIN_DAYS": 320, "COLOR": (255, 255, 0)},
    34: {"STATE": "GEN_34", "MIN_DAYS": 330, "COLOR": (255, 223, 0)},
    35: {"STATE": "GEN_35", "MIN_DAYS": 340, "COLOR": (255, 191, 0)},
    36: {"STATE": "GEN_36", "MIN_DAYS": 350, "COLOR": (255, 159, 0)},
    37: {"STATE": "GEN_37", "MIN_DAYS": 360, "COLOR": (255, 127, 0)},
    38: {"STATE": "GEN_38", "MIN_DAYS": 370, "COLOR": (255, 95, 0)},
    39: {"STATE": "GEN_39", "MIN_DAYS": 380, "COLOR": (255, 63, 0)},
    40: {"STATE": "GEN_40", "MIN_DAYS": 390, "COLOR": (255, 31, 0)},
    41: {"STATE": "GEN_41", "MIN_DAYS": 400, "COLOR": (255, 0, 0)},
}


MIN_WINDOW_SIZE = (640, 360)

MAX_DAY_COUNT = 500

COLOR_PLAY_SURFACE_BACKGROUND = (1, 0, 0)
# IMPORTANT: If not None, this color needs to be different from other Cell colors
COLOR_PLAY_SURFACE_COLORKEY = COLOR_PLAY_SURFACE_BACKGROUND # COLOR_PLAYSURFACE_BACKGROUND | None
