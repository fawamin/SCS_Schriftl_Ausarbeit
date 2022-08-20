import settings
import pygame
import pygame_menu
import pygame_menu.widgets
import pygame_menu.themes
import pygame_menu.events
import pygame_menu.locals
import os

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
    menuPlay: pygame_menu.Menu
    menuMain: pygame_menu.Menu
    dGOL: DisplayGameOfLife

    def __init__(self):
        """
        Main function of the program.
        """
        # Initialize Pygame if not already initialized
        if not pygame.get_init():
            pygame.init()
        # Create the screencd
        screen = pygame.display.set_mode(settings.WINDOW_SIZE, pygame.RESIZABLE)
        # Clock for managing the FPS
        clock = pygame.time.Clock()
        # Set the window title
        pygame.display.set_caption(settings.CAPTION_BASE)
        # create DisplayGOL instance
        self.dGOL = DisplayGameOfLife(screen)


        # -------------------------------------------------------------------------
        # Create menus: Play Menu
        # -------------------------------------------------------------------------
        self.menuPlay = pygame_menu.Menu(
            settings.CAPTION_BASE,
            screen.get_width(),
            screen.get_height(),
            # mouse_motion_selection=True,
            theme = pygame_menu.themes.THEME_DARK.copy(),
            columns = 2,
            rows = [5, 8],
        )
        self.menuPlay._disable_widget_update_mousepos_mouseselection = True

        vMargin = 30
        validIntChars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        self.menuPlay.add.toggle_switch("infinity play area: ", settings.DEFAULT_INFINITY_PLAY_AREA, toggleswitch_id = "infinityPlayArea")
        self.menuPlay.add.text_input("Cell size (px): ", settings.DEFAULT_CELL_SIZE, input_type = pygame_menu.locals.INPUT_INT, valid_chars = validIntChars, maxchar = 3, textinput_id = "cellSize")
        self.menuPlay.add.text_input("Cell margin (px): ", settings.DEFAULT_CELL_MARGIN, input_type = pygame_menu.locals.INPUT_INT, valid_chars = validIntChars, maxchar = 2, textinput_id = "cellMargin")
        self.menuPlay.add.text_input("Cell border radius (px): ", settings.DEFAULT_CELL_BORDER_RADIUS, input_type = pygame_menu.locals.INPUT_INT, valid_chars = validIntChars, maxchar = 2, textinput_id = "cellBorderRadius")
        self.menuPlay.add.text_input("Cell hover border width (px): ", settings.DEFAULT_CELL_HOVER_BORDER_WIDTH, input_type = pygame_menu.locals.INPUT_INT, valid_chars = validIntChars, maxchar = 2, textinput_id = "cellHoverBorderWidth")

        self.menuPlay.add.text_input("Rows: ", settings.DEFAULT_ROWS, input_type = pygame_menu.locals.INPUT_INT, valid_chars = validIntChars, textinput_id = "rows")
        self.menuPlay.add.text_input("Columns: ", settings.DEFAULT_COLS, input_type = pygame_menu.locals.INPUT_INT, valid_chars = validIntChars, textinput_id = "cols")
        self.menuPlay.add.button('Start with Setting', self._startGameFromSttings)

        self.menuPlay.add.vertical_margin(vMargin)
        try:
            saveFiles = [(file,) for file in os.listdir(settings.DIR_SAVE) if file.endswith(".npy")]
        except FileNotFoundError:
            saveFiles = []
            self.menuPlay.add.label("Directory not found")
        else:
            if len(saveFiles) > 0:
                self.menuPlay.add.dropselect("File: ", saveFiles, dropselect_id = "saveFile")
            else:
                self.menuPlay.add.label("No save files found")
        self.menuPlay.add.button('Start From File', self._startGameFromFile)

        self.menuPlay.add.vertical_margin(vMargin)
        self.menuPlay.add.button('Return to main menu', pygame_menu.events.BACK)


        # -------------------------------------------------------------------------
        # Create menus: About
        # -------------------------------------------------------------------------
        menuAbout = pygame_menu.Menu(
            settings.TITLE_ABOUT,
            screen.get_width(),
            screen.get_height(),
            mouse_motion_selection=True,
            theme = pygame_menu.themes.THEME_DARK.copy(),
        )
        menuAbout._disable_widget_update_mousepos_mouseselection = True

        for about in settings.ABOUT:
          menuAbout.add.label(about, align=pygame_menu.locals.ALIGN_CENTER, font_size=settings.FONT_SIZE)
        menuAbout.add.vertical_margin(30)
        menuAbout.add.button('Return to menu', pygame_menu.events.BACK)

    
        # -------------------------------------------------------------------------
        # Create menus: Main
        # -------------------------------------------------------------------------
        self.menuMain = pygame_menu.Menu(
            settings.TITLE_MAIN_MENU,
            screen.get_width(),
            screen.get_height(),
            mouse_motion_selection=True,
            theme = pygame_menu.themes.THEME_DARK.copy(),
        )
        self.menuMain._disable_widget_update_mousepos_mouseselection = True

        self.menuMain.add.button('Play', self.menuPlay)
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
                elif event.type == pygame.VIDEORESIZE:
                    width, height = screen.get_size()
                    minWidth, minHeight = settings.MIN_WINDOW_SIZE
                    if width < minWidth or height < minHeight:
                        if width < minWidth:
                            width = minWidth
                        if height < minHeight:
                            height = minHeight
                        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                    self.menuMain.resize(width, height)
                    self.menuPlay.resize(width, height)
                    menuAbout.resize(width, height)
                    self.dGOL.resize(width, height)

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
        rows = None
        cols = None
        infinityPlayArea = None
        cellSize = None
        cellMargin = None
        cellBorderRadius = None
        cellHoverBorderWidth = None
        
        data = self.menuPlay.get_input_data()
        for key in data:
            print(key, data[key])
            if key == "rows":
                if int(data[key]) > 0:
                    rows = int(data[key])
            elif key == "cols":
                if int(data[key]) > 0:
                    cols = int(data[key])
            elif key == "infinityPlayArea":
                infinityPlayArea = bool(data[key])
            elif key == "cellSize":
                if int(data[key]) > 0:
                    cellSize = int(data[key])
            elif key == "cellMargin":
                cellMargin = int(data[key])
            elif key == "cellBorderRadius":
                cellBorderRadius = int(data[key])
            elif key == "cellHoverBorderWidth":
                cellHoverBorderWidth = int(data[key])

        # Check if all values are set (if not set menans that the settings are not valid and the game should not be started)
        if rows is not None and cols is not None and infinityPlayArea is not None and cellSize is not None and cellMargin is not None and cellBorderRadius is not None and cellHoverBorderWidth is not None:
            self.dGOL.startGameFromSettings(rows, cols, infinityPlayArea, cellSize, cellMargin, cellBorderRadius, cellHoverBorderWidth, self.menuMain)


    def _startGameFromFile(self):
        """
        Start the game from a file.
        """
        saveFile = None
        infinityPlayArea = None
        cellSize = None
        cellMargin = None
        cellBorderRadius = None
        cellHoverBorderWidth = None

        data = self.menuPlay.get_input_data()
        for key in data:
            if key == "saveFile":
                saveFile = "Pygame/Saves/" + data[key][0][0]
            elif key == "infinityPlayArea":
                infinityPlayArea = bool(data[key])
            elif key == "cellSize":
                if int(data[key]) > 0:
                    cellSize = int(data[key])
            elif key == "cellMargin":
                cellMargin = int(data[key])
            elif key == "cellBorderRadius":
                cellBorderRadius = int(data[key])
            elif key == "cellHoverBorderWidth":
                cellHoverBorderWidth = int(data[key])

        # Check if all values are set (if not set menans that the settings are not valid and the game should not be started)
        if saveFile is not None and infinityPlayArea is not None and cellSize is not None and cellMargin is not None and cellBorderRadius is not None and cellHoverBorderWidth is not None:
            self.dGOL.startGameFromFile(saveFile, infinityPlayArea, cellSize, cellMargin, cellBorderRadius, cellHoverBorderWidth, self.menuMain)


if __name__ == '__main__':
    DisplayGameOfLifeMenu()
