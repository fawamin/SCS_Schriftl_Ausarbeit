from matplotlib.pyplot import cla
import numpy as np
import pygame
import sys

import pygame_menu

from GameOfLife import GameOfLife
import settings
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE
)

pygame.init()


class DisplayGOL:

    gol = None
    dw = None
    dh = None
    coldead = (255,255,255)
    colalive = (0,0,0)

    def __init__(self, displaywidth, displayheight):
        self.gol = GameOfLife()
        self.dw = displaywidth
        self.dh = displayheight
        self.screen = pygame.display.set_mode((displaywidth, displayheight))

    def TestPeparationMethod(self):
        self.gol.setSaveFile("Saves/5x5test.npy")
        self.gol.loadFileData() 
        #DAYEVENT is event type thats user generated
        DAYEVENT  = pygame.USEREVENT+1
        # cyclelenght is the lenght in ms 
        cyclelenght = 500
        # Sets a Timer that triggers the DAYEVENT every cyclelenght ms
        pygame.time.set_timer(DAYEVENT,cyclelenght)
        running = True
        #Render Screen once before first Cycle
        self.renderScreen(self.screen)
        while running:
            self.renderScreen(self.screen)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False
                if event.type == DAYEVENT:
                    self.gol.cycleDay()
                    self.renderScreen(self.screen)



    def renderScreen(self, screen):
        screen.fill((255, 255, 255))
        field = self.gol.getField()
        rows, cols = field.shape
        # Find Width and Height of each Square
        width = self.dw / rows
        height = self.dh / cols
        for row, col in np.ndindex(field.shape):
            #Is Cell Dead or Alive?
            if field[row,col] == 0:
                colour = self.coldead
            elif field[row,col] == 1:
                colour = self.colalive
            #Draw Cell
            pygame.draw.rect(screen,colour,(row * width - 2 ,col * height -2 , width -2 , height- 2))
        #Update display
        pygame.display.update()



# di = DisplayGOL(600, 600)
# di.TestPeparationMethod()


def main():
    """
    Main function of the program.
    """
    # Initialize Pygame
    pygame.init()
    # Create the screen
    screen = pygame.display.set_mode(settings.WINDOW_SIZE)
    # Clock for managing the FPS
    clock = pygame.time.Clock()
    # Set the window title
    pygame.display.set_caption(settings.CAPTION_BASE)
    

    # -------------------------------------------------------------------------
    # Create menus: Play Menu
    # -------------------------------------------------------------------------
    menuPlay = pygame_menu.Menu(
        settings.CAPTION_BASE,
        settings.WINDOW_WIDTH,
        settings.WINDOW_HEIGHT,
        mouse_motion_selection=True,
        theme = pygame_menu.themes.THEME_DARK.copy(),
        columns = 2,
        rows = [2, 1],
    )
    menuPlay._disable_widget_update_mousepos_mouseselection = True

    menuPlay.add.button('Start',  # When pressing return -> play(DIFFICULTY[0], font) \n play_function,\nDIFFICULTY,\n pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30)
                         pygame_menu.events.BACK)
    menuPlay.add.button('Return to main menu', pygame_menu.events.BACK)

    gol = GameOfLife()
    gol.setSaveFile(settings.SAVE_FILE)
    gol.loadFileData()
    #DAYEVENT is event type thats user generated
    DAYEVENT  = pygame.USEREVENT+1
    # cyclelenght is the lenght in ms 
    cyclelenght = 500
    # Sets a Timer that triggers the DAYEVENT every cyclelenght ms
    pygame.time.set_timer(DAYEVENT,cyclelenght)
    running = True
    #Render Screen once before first Cycle
    playSurface = pygame.Surface(size = (500, 500))
    # playSurface.subsurface(left_top = (50, 100), width_height = (400, 400))
    renderSurface(playSurface, gol.getField())

    playWidget = menuPlay.add.surface(playSurface, selectable = True, selection_effect = pygame_menu.widgets.NoneSelection())
    playWidget.set_col_row_index(1, 0, 2)
    print(playWidget.get_col_row_index())

    # -------------------------------------------------------------------------
    # Create menus: About
    # -------------------------------------------------------------------------
    menuAbout = pygame_menu.Menu(
        settings.TITLE_ABOUT,
        settings.WINDOW_WIDTH,
        settings.WINDOW_HEIGHT,
        mouse_motion_selection=True,
        theme = pygame_menu.themes.THEME_DARK.copy(),
    )
    menuAbout._disable_widget_update_mousepos_mouseselection = True

    for about in settings.ABOUT:
        menuAbout.add.label(about, align=pygame_menu.locals.ALIGN_LEFT, font_size=settings.FONT_SIZE)
    menuAbout.add.vertical_margin(30)
    menuAbout.add.button('Return to menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus: Main
    # -------------------------------------------------------------------------
    menuMain = pygame_menu.Menu(
        settings.TITLE_MAIN_MENU,
        settings.WINDOW_WIDTH,
        settings.WINDOW_HEIGHT,
        mouse_motion_selection=True,
        theme = pygame_menu.themes.THEME_DARK.copy(),
    )
    menuMain._disable_widget_update_mousepos_mouseselection = True

    menuMain.add.button('Play', menuPlay)
    menuMain.add.button('About', menuAbout)
    menuMain.add.button('Quit', pygame_menu.events.EXIT)
    
    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:
        #Tick
        clock.tick(settings.FPS)
    
        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == DAYEVENT:
                gol.cycleDay()
                renderSurface(playSurface, gol.getField())
                playWidget.force_menu_surface_update()

        # Main menu
        if menuMain.is_enabled():
            menuMain.update(events)
            menuMain.draw(screen)

        # Flip surface
        pygame.display.flip()
    
    # Close the window and quit.
    pygame.quit()
    sys.exit()

def renderSurface(surface: pygame.Surface, field: np.ndarray):
    surface.fill(settings.COLOR_PLAYSURFACE_BACKGROUND)
    surface.set_colorkey(settings.COLOR_PLAYSURFACE_COLORKEY)
    #surface.set_alpha(128)
    rows, cols = field.shape
    # Find Width and Height of each Square
    width = surface.get_width() / rows
    height = surface.get_height() / cols
    for row, col in np.ndindex(field.shape):
        #Is Cell Dead or Alive?
        if field[row,col] == 0:
            colour = settings.COLOR_DEATH
        elif field[row,col] == 1:
            colour = settings.COLOR_ALIVE
        #Draw Cell
        pygame.draw.rect(surface, colour, (row * width + 1, col * height + 1, width - 2, height - 2), border_radius = 10)

if __name__ == '__main__':
    main()