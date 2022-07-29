import pygame
import pygame_menu

WINDOW_SIZE = {
    "WGA":(854, 480),
    "HD": (1280, 720),
    "FHD": (1920, 1080),
    "UWFHD": (2560, 1080),
    "WQHD": (2560, 1440),
    "UWQHD": (3440, 1440),
    "UHD": (3840, 2160),
    "coustum": (1600, 900),
}["coustum"]

WINDOW_WIDTH, WINDOW_HEIGHT = WINDOW_SIZE

FPS = 60

TITLE_MAIN_MENU = "Main Menu"
TITLE_ABOUT = "About"

CAPTION_BASE = "GameOfLife"
CAPTION_MAIN_MENU = CAPTION_BASE + " - " + TITLE_MAIN_MENU
CAPTION_ABOUT = CAPTION_BASE + " - " + TITLE_ABOUT

ABOUT = [
    f'Author: Steffen Hill',
    f'Pygame {pygame.__version__}',
    f'pygame-menu {pygame_menu.__version__}'
    ]

FONT_SIZE = 20

COLOR_BACKGROUND = (25, 25, 25)
COLOR_DEATH = (0,0,0)
COLOR_ALIVE = (255,255,255)

COLOR_PLAYSURFACE_BACKGROUND = (1, 0, 0)
# IMPORTANT: If not None, this color needs to be different from other Cell colors
COLOR_PLAYSURFACE_COLORKEY = COLOR_PLAYSURFACE_BACKGROUND # COLOR_PLAYSURFACE_BACKGROUND | None

SAVE_FILE = [
    "Saves/3x3.npy",
    "Saves/5x5test.npy",
    "Saves/10x10Glider.npy",
    "Saves/64x64.npy",
    "Saves/test.npy"
    ][1]