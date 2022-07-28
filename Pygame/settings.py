import pygame
import pygame_menu

WINDOW_SIZE = (WINDOW_WIDTH:=800, WINDOW_HEIGHT:=600)

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