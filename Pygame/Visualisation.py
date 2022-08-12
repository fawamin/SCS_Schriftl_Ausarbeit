import settings
import pygame
import pygame_menu
import pygame_menu.widgets
import pygame_menu.themes
import pygame_menu.events
import pygame_menu.locals

from DisplayGameOfLife import DisplayGameOfLife
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

class DisplayGameOfLifeMenu:
    menuMain: pygame_menu.Menu
    dGOL: DisplayGameOfLife

    def __init__(self):
        """
        Main function of the program.
        """
        # Initialize Pygame if not already initialized
        if not pygame.get_init():
            pygame.init()
        # Create the screen
        screen = pygame.display.set_mode(settings.WINDOW_SIZE)
        # Clock for managing the FPS
        clock = pygame.time.Clock()
        # Set the window title
        pygame.display.set_caption(settings.CAPTION_BASE)
        # create DisplayGOL instance
        self.dGOL = DisplayGameOfLife(screen)


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

        menuPlay.add.button('Start with Setting', self._startGameFromSttings)
        menuPlay.add.button('Start From File', self._startGameFromFile)
        menuPlay.add.button('Return to main menu', pygame_menu.events.BACK)


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
        self.menuMain = pygame_menu.Menu(
            settings.TITLE_MAIN_MENU,
            settings.WINDOW_WIDTH,
            settings.WINDOW_HEIGHT,
            mouse_motion_selection=True,
            theme = pygame_menu.themes.THEME_DARK.copy(),
        )
        self.menuMain._disable_widget_update_mousepos_mouseselection = True

        self.menuMain.add.button('Play', menuPlay)
        self.menuMain.add.button('About', menuAbout)
        self.menuMain.add.button('Quit', pygame_menu.events.EXIT)


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
                    pygame.quit()
                    exit()
            if event.type == DAYEVENT:
                gol.cycleDay()
                renderSurface(playSurface, gol.getField())
                playWidget.force_menu_surface_update()

            # Main menu
            if self.menuMain.is_enabled():
                self.menuMain.draw(screen)
                self.menuMain.update(events)

            if self.dGOL.is_enabled():
                self.dGOL.draw()
                self.dGOL.update(events)

            # Flip surface
            pygame.display.flip()


    def _startGameFromSttings(self):
        """
        Start the game from settings.
        """
        self.dGOL.startGameFromSettings(
            settings.DEFAULT_ROWS, 
            settings.DEFAULT_COLS,
            settings.DEFAULT_INFINITY_PLAY_AREA, 
            settings.DEFAULT_CELL_SIZE, 
            settings.DEFAULT_CELL_MARGIN, 
            settings.DEFAULT_CELL_BORDER_RADIUS, 
            settings.DEFAULT_CELL_HOVER_BORDER_WIDTH, 
            self.menuMain)


    def _startGameFromFile(self):
        """
        Start the game from a file.
        """
        self.dGOL.startGameFromFile(
            settings.SAVE_FILE, 
            True,#settings.DEFAULT_INFINITY_PLAY_AREA, 
            settings.DEFAULT_CELL_SIZE, 
            settings.DEFAULT_CELL_MARGIN, 
            settings.DEFAULT_CELL_BORDER_RADIUS, 
            5, #settings.DEFAULT_CELL_HOVER_BORDER_WIDTH, 
            self.menuMain)


if __name__ == '__main__':
    DisplayGameOfLifeMenu()
