from faulthandler import is_enabled
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
    menuAbout: pygame_menu.Menu
    
    menuFromFile: pygame_menu.Menu
    menuFromSettings: pygame_menu.Menu

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

        #Menu Creation
        self.createFromSettingsMenu(screen)
        self.createFromFileMenu(screen)
        
        self.createStartMenu(screen)
        self.createAboutMenu(screen)

        self.createMainMenu(screen)
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
                    self.menuAbout.resize(width, height)
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


    def _startGameFromSettings(self):
        """
        Start the game from settings.
        """
        cols = None
        rows = None
        infinityPlayArea = None
        cellSize = None
        cellMargin = None
        cellBorderRadius = None
        cellHoverBorderWidth = None

        data = self.menuFromSettings.get_input_data()
        for key in data:
            if key == "cols":
                if int(data[key]) > 0:
                    cols = int(data[key])
            elif key == "rows":
                if int(data[key]) > 0:
                    rows = int(data[key])
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
        if cols is not None and rows is not None and infinityPlayArea is not None and cellSize is not None and cellMargin is not None and cellBorderRadius is not None and cellHoverBorderWidth is not None:
            self.dGOL.startGameFromSettings(cols, rows, infinityPlayArea, cellSize, cellMargin, cellBorderRadius, cellHoverBorderWidth, self.menuMain)


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

        data = self.menuFromFile.get_input_data()
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


    #Menu where Selection between Loading and creating new game happens
    def createStartMenu(self,screen):
        self.menuPlay = pygame_menu.Menu(
            settings.CAPTION_BASE,
            screen.get_width(),
            screen.get_height(),
            mouse_motion_selection=True,
            theme = pygame_menu.themes.THEME_DARK.copy(),
            columns = 2,
            rows = [5, 8],
        )
        self.menuPlay._disable_widget_update_mousepos_mouseselection = True

        vMargin = 30
        self.menuPlay.add.button('Create new', self.menuFromSettings)
        self.menuPlay.add.button('Load File', self.menuFromFile)
        self.menuPlay.add.vertical_margin(vMargin)
        self.menuPlay.add.button('Return to main menu', pygame_menu.events.BACK)

    def createFromFileMenu(self,screen):
        self.menuFromFile = pygame_menu.Menu(
            settings.TITLE_FROMFILE,
            screen.get_width(),
            screen.get_height(),
            mouse_motion_selection=True,
            theme = pygame_menu.themes.THEME_DARK.copy(),
        )

        self.menuFromFile.add.toggle_switch("infinity play area: ", settings.DEFAULT_INFINITY_PLAY_AREA, toggleswitch_id = "infinityPlayArea")
        self.menuFromFile.add.text_input("Cell size (px): ", settings.DEFAULT_CELL_SIZE, input_type = pygame_menu.locals.INPUT_INT, valid_chars = settings.VALIDINTCHARS, maxchar = 3, textinput_id = "cellSize", input_underline="_", input_underline_len = 4)
        self.menuFromFile.add.text_input("Cell margin (px): ", settings.DEFAULT_CELL_MARGIN, input_type = pygame_menu.locals.INPUT_INT, valid_chars = settings.VALIDINTCHARS, maxchar = 2, textinput_id = "cellMargin", input_underline="_", input_underline_len = 3)
        self.menuFromFile.add.text_input("Cell border radius (px): ", settings.DEFAULT_CELL_BORDER_RADIUS, input_type = pygame_menu.locals.INPUT_INT, valid_chars = settings.VALIDINTCHARS, maxchar = 2, textinput_id = "cellBorderRadius", input_underline="_", input_underline_len = 3)
        self.menuFromFile.add.text_input("Cell hover border width (px): ", settings.DEFAULT_CELL_HOVER_BORDER_WIDTH, input_type = pygame_menu.locals.INPUT_INT, valid_chars = settings.VALIDINTCHARS, maxchar = 2, textinput_id = "cellHoverBorderWidth", input_underline="_", input_underline_len = 3)

        #Savefile list
        try:
            saveFiles = [(file,) for file in os.listdir(settings.DIR_SAVE) if file.endswith(".npy")]
        except FileNotFoundError:
            saveFiles = []
            self.menuFromFile.add.label("Directory not found")
        else:
            if len(saveFiles) > 0:
                select = self.menuFromFile.add.dropselect("File: ", saveFiles, dropselect_id="saveFile")
                select.force_menu_surface_update()

                self.menuFromFile.set_onbeforeopen(self.update_List)
            else:
                self.menuFromFile.add.label("No save files found")

        #Start the Game
        self.menuFromFile.add.button('Load', self._startGameFromFile)

        #Return to last menu
        self.menuFromFile.add.button('Back', pygame_menu.events.BACK)

    def update_List(self,*kwarg):
        saveFiles = [(file,) for file in os.listdir(settings.DIR_SAVE) if file.endswith(".ny")]
        if len(saveFiles) > 0:
            self.menuFromFile.get_widget("saveFile").reset_value
            self.menuFromFile.get_widget("saveFile").update_items(saveFiles)
            print("test")
            #widget.update_items(saveFiles)
            


    def createFromSettingsMenu(self,screen):
        self.menuFromSettings = pygame_menu.Menu(
            settings.TITLE_FROMSETTINGS,
            screen.get_width(),
            screen.get_height(),
            mouse_motion_selection=True,
            theme = pygame_menu.themes.THEME_DARK.copy(),
        )

        #Options for Creation of new Playing Area
        self.menuFromSettings.add.toggle_switch("infinity play area: ", settings.DEFAULT_INFINITY_PLAY_AREA, toggleswitch_id = "infinityPlayArea")
        self.menuFromSettings.add.text_input("Cell size (px): ", settings.DEFAULT_CELL_SIZE, input_type = pygame_menu.locals.INPUT_INT, valid_chars = settings.VALIDINTCHARS, maxchar = 3, textinput_id = "cellSize", input_underline="_", input_underline_len = 4)
        self.menuFromSettings.add.text_input("Cell margin (px): ", settings.DEFAULT_CELL_MARGIN, input_type = pygame_menu.locals.INPUT_INT, valid_chars = settings.VALIDINTCHARS, maxchar = 2, textinput_id = "cellMargin", input_underline="_", input_underline_len = 3)
        self.menuFromSettings.add.text_input("Cell border radius (px): ", settings.DEFAULT_CELL_BORDER_RADIUS, input_type = pygame_menu.locals.INPUT_INT, valid_chars = settings.VALIDINTCHARS, maxchar = 2, textinput_id = "cellBorderRadius", input_underline="_", input_underline_len = 3)
        self.menuFromSettings.add.text_input("Cell hover border width (px): ", settings.DEFAULT_CELL_HOVER_BORDER_WIDTH, input_type = pygame_menu.locals.INPUT_INT, valid_chars = settings.VALIDINTCHARS, maxchar = 2, textinput_id = "cellHoverBorderWidth", input_underline="_", input_underline_len = 3)
        
        #Playarea Size
        self.menuFromSettings.add.text_input("Columns: ", settings.DEFAULT_COLS, input_type = pygame_menu.locals.INPUT_INT, valid_chars = settings.VALIDINTCHARS, textinput_id = "cols", input_underline="_", input_underline_len = 4)
        self.menuFromSettings.add.text_input("Rows: ", settings.DEFAULT_ROWS, input_type = pygame_menu.locals.INPUT_INT, valid_chars = settings.VALIDINTCHARS, textinput_id = "rows", input_underline="_", input_underline_len = 4)
        self.menuFromSettings.add.button('Start', self._startGameFromSettings)
        self.menuFromSettings.add.button('Back', pygame_menu.events.BACK)

    #Menu With information about the Program
    def createAboutMenu(self,screen):
        self.menuAbout = pygame_menu.Menu(
            settings.TITLE_ABOUT,
            screen.get_width(),
            screen.get_height(),
            mouse_motion_selection=True,
            theme = pygame_menu.themes.THEME_DARK.copy(),
        )
        self.menuAbout._disable_widget_update_mousepos_mouseselection = True

        for about in settings.ABOUT:
          self.menuAbout.add.label(about, align=pygame_menu.locals.ALIGN_CENTER, font_size=settings.FONT_SIZE)
        self.menuAbout.add.vertical_margin(30)
        self.menuAbout.add.button('Return to menu', pygame_menu.events.BACK)

    def createMainMenu(self,screen):
            self.menuMain = pygame_menu.Menu(
                settings.TITLE_MAIN_MENU,
                screen.get_width(),
                screen.get_height(),
                mouse_motion_selection=True,
                theme = pygame_menu.themes.THEME_DARK.copy(),
            )
            self.menuMain._disable_widget_update_mousepos_mouseselection = True

            self.menuMain.add.button('Play', self.menuPlay)
            self.menuMain.add.button('About', self.menuAbout)
            self.menuMain.add.button('Quit', pygame_menu.events.EXIT)



if __name__ == '__main__':
    DisplayGameOfLifeMenu()
