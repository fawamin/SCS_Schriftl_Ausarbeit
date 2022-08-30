import Settings
import pygame
import pygame_menu
import pygame_menu.widgets
import pygame_menu.themes
import pygame_menu.events
import pygame_menu.locals
import os

from DisplayGameOfLife import DisplayGameOfLife


class DisplayGameOfLifeMenu:
    _screen: pygame.Surface

    _menuPlay: pygame_menu.Menu
    _menuMain: pygame_menu.Menu
    _menuAbout: pygame_menu.Menu
    _menuFromFile: pygame_menu.Menu
    _menuFromSettings: pygame_menu.Menu

    _dGOL: DisplayGameOfLife

    def __init__(self):
        """
        Main function of the program.
        """
        # Initialize Pygame if not already initialized
        if not pygame.get_init():
            pygame.init()
        # Create the screen
        self._screen = pygame.display.set_mode(Settings.WINDOW_SIZE, pygame.RESIZABLE)
        # Clock for managing the FPS
        clock = pygame.time.Clock()
        # Set the window title
        pygame.display.set_caption(Settings.TITLE_BASE)
        # create DisplayGOL instance
        self._dGOL = DisplayGameOfLife(self._screen)

        #Menu Creation
        self._createFromSettingsMenu()
        self._createFromFileMenu()

        self._createStartMenu()
        self._createAboutMenu()

        self._createMainMenu()
        # -------------------------------------------------------------------------
        # Main loop
        # -------------------------------------------------------------------------
        while True:
            #Tick
            clock.tick(Settings.FPS)

            # Application events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.VIDEORESIZE:
                    width, height = self._screen.get_size()
                    minWidth, minHeight = Settings.MIN_WINDOW_SIZE
                    if width < minWidth or height < minHeight:
                        if width < minWidth:
                            width = minWidth
                        if height < minHeight:
                            height = minHeight
                        self._screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                    self._menuMain.resize(width, height)
                    self._menuPlay.resize(width, height)
                    self._menuAbout.resize(width, height)
                    self._menuFromFile.resize(width, height)
                    self._menuFromSettings.resize(width, height)
                    self._dGOL.resize(width, height)

            # Main menu
            if self._menuMain.is_enabled():
                self._menuMain.draw(self._screen)
                self._menuMain.update(events)

            if self._dGOL.is_enabled():
                self._dGOL.draw()
                self._dGOL.update(events)

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

        data = self._menuFromSettings.get_input_data()
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
            self._dGOL.startGameFromSettings(cols, rows, infinityPlayArea, cellSize, cellMargin, cellBorderRadius, cellHoverBorderWidth, self._menuMain)


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

        data = self._menuFromFile.get_input_data()
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
            self._dGOL.startGameFromFile(saveFile, infinityPlayArea, cellSize, cellMargin, cellBorderRadius, cellHoverBorderWidth, self._menuMain)


    #Menu where Selection between Loading and creating new game happens
    def _createStartMenu(self):
        self._menuPlay = pygame_menu.Menu(
            Settings.TITLE_BASE,
            self._screen.get_width(),
            self._screen.get_height(),
            mouse_motion_selection = True,
            theme = pygame_menu.themes.THEME_DARK.copy(),
        )
        self._menuPlay._disable_widget_update_mousepos_mouseselection = True

        vMargin = 30
        self._menuPlay.add.button('New Game', self._menuFromSettings)
        self._menuPlay.add.button('Load File', self._menuFromFile)
        self._menuPlay.add.vertical_margin(vMargin)
        self._menuPlay.add.button('Back', pygame_menu.events.BACK)


    def _createFromFileMenu(self):
        self._menuFromFile = pygame_menu.Menu(
            Settings.TITLE_FROMFILE,
            self._screen.get_width(),
            self._screen.get_height(),
            mouse_motion_selection = True,
            theme = pygame_menu.themes.THEME_DARK.copy(),
        )

        self._menuFromFile.add.toggle_switch("infinity play area: ", Settings.DEFAULT_INFINITY_PLAY_AREA, toggleswitch_id = "infinityPlayArea")
        self._menuFromFile.add.text_input("Cell size (px): ", Settings.DEFAULT_CELL_SIZE, input_type = pygame_menu.locals.INPUT_INT, valid_chars = Settings.VALIDINTCHARS, maxchar = 3, textinput_id = "cellSize", input_underline="_", input_underline_len = 4)
        self._menuFromFile.add.text_input("Cell margin (px): ", Settings.DEFAULT_CELL_MARGIN, input_type = pygame_menu.locals.INPUT_INT, valid_chars = Settings.VALIDINTCHARS, maxchar = 2, textinput_id = "cellMargin", input_underline="_", input_underline_len = 3)
        self._menuFromFile.add.text_input("Cell border radius (px): ", Settings.DEFAULT_CELL_BORDER_RADIUS, input_type = pygame_menu.locals.INPUT_INT, valid_chars = Settings.VALIDINTCHARS, maxchar = 2, textinput_id = "cellBorderRadius", input_underline="_", input_underline_len = 3)
        self._menuFromFile.add.text_input("Cell hover border width (px): ", Settings.DEFAULT_CELL_HOVER_BORDER_WIDTH, input_type = pygame_menu.locals.INPUT_INT, valid_chars = Settings.VALIDINTCHARS, maxchar = 2, textinput_id = "cellHoverBorderWidth", input_underline="_", input_underline_len = 3)

        #Savefile list
        saveFiles = [("No file",)] # Placeholder because the list can't be empty (before the menu is opened the list of files gets loaded)
        saveFileDropSelect: pygame_menu.widgets.Widget = self._menuFromFile.add.dropselect("File: ", saveFiles, dropselect_id = "saveFile")
        noFileLabel: pygame_menu.widgets.Widget = self._menuFromFile.add.label("No save files found", "noFileLabel")
        noFileLabel.hide()
        saveFileDropSelect.show()
        self._menuFromFile.set_onbeforeopen(self._updateSaveFileList)

        #Start the Game
        self._menuFromFile.add.button('Load', self._startGameFromFile)

        #Return to last menu
        self._menuFromFile.add.button('Back', pygame_menu.events.BACK)


    def _updateSaveFileList(self, *kwarg):
        saveFileDropSelect = self._menuFromFile.get_widget("saveFile")
        noFileLabel = self._menuFromFile.get_widget("noFileLabel")
        if saveFileDropSelect is not None and noFileLabel is not None:
            saveFileDropSelect.reset_value()
            try:
                saveFiles = [(file,) for file in os.listdir(Settings.DIR_SAVE) if file.endswith(".npy")]
            except FileNotFoundError:
                saveFiles = []
            if len(saveFiles) > 0:
                saveFileDropSelect.update_items(saveFiles)
                noFileLabel.hide()
                saveFileDropSelect.show()
                saveFileDropSelect.force_menu_surface_update()
            else:
                noFileLabel.show()
                saveFileDropSelect.hide()


    def _createFromSettingsMenu(self):
        self._menuFromSettings = pygame_menu.Menu(
            Settings.TITLE_FROMSETTINGS,
            self._screen.get_width(),
            self._screen.get_height(),
            mouse_motion_selection = True,
            theme = pygame_menu.themes.THEME_DARK.copy(),
        )

        #Options for Creation of new Playing Area
        self._menuFromSettings.add.toggle_switch("infinity play area: ", Settings.DEFAULT_INFINITY_PLAY_AREA, toggleswitch_id = "infinityPlayArea")
        self._menuFromSettings.add.text_input("Cell size (px): ", Settings.DEFAULT_CELL_SIZE, input_type = pygame_menu.locals.INPUT_INT, valid_chars = Settings.VALIDINTCHARS, maxchar = 3, textinput_id = "cellSize", input_underline="_", input_underline_len = 4)
        self._menuFromSettings.add.text_input("Cell margin (px): ", Settings.DEFAULT_CELL_MARGIN, input_type = pygame_menu.locals.INPUT_INT, valid_chars = Settings.VALIDINTCHARS, maxchar = 2, textinput_id = "cellMargin", input_underline="_", input_underline_len = 3)
        self._menuFromSettings.add.text_input("Cell border radius (px): ", Settings.DEFAULT_CELL_BORDER_RADIUS, input_type = pygame_menu.locals.INPUT_INT, valid_chars = Settings.VALIDINTCHARS, maxchar = 2, textinput_id = "cellBorderRadius", input_underline="_", input_underline_len = 3)
        self._menuFromSettings.add.text_input("Cell hover border width (px): ", Settings.DEFAULT_CELL_HOVER_BORDER_WIDTH, input_type = pygame_menu.locals.INPUT_INT, valid_chars = Settings.VALIDINTCHARS, maxchar = 2, textinput_id = "cellHoverBorderWidth", input_underline="_", input_underline_len = 3)

        #Playarea Size
        self._menuFromSettings.add.text_input("Columns: ", Settings.DEFAULT_COLS, input_type = pygame_menu.locals.INPUT_INT, valid_chars = Settings.VALIDINTCHARS, textinput_id = "cols", input_underline="_", input_underline_len = 4)
        self._menuFromSettings.add.text_input("Rows: ", Settings.DEFAULT_ROWS, input_type = pygame_menu.locals.INPUT_INT, valid_chars = Settings.VALIDINTCHARS, textinput_id = "rows", input_underline="_", input_underline_len = 4)
        self._menuFromSettings.add.button('Start', self._startGameFromSettings)
        self._menuFromSettings.add.button('Back', pygame_menu.events.BACK)


    #Menu With information about the Program
    def _createAboutMenu(self):
        self._menuAbout = pygame_menu.Menu(
            Settings.TITLE_ABOUT,
            self._screen.get_width(),
            self._screen.get_height(),
            mouse_motion_selection = True,
            theme = pygame_menu.themes.THEME_DARK.copy(),
        )
        self._menuAbout._disable_widget_update_mousepos_mouseselection = True

        for about in Settings.ABOUT:
          self._menuAbout.add.label(about, align=pygame_menu.locals.ALIGN_CENTER, font_size=Settings.FONT_SIZE)
        self._menuAbout.add.vertical_margin(30)
        self._menuAbout.add.button('Return to menu', pygame_menu.events.BACK)


    def _createMainMenu(self):
            self._menuMain = pygame_menu.Menu(
                Settings.TITLE_MAIN_MENU,
                self._screen.get_width(),
                self._screen.get_height(),
                mouse_motion_selection = True,
                theme = pygame_menu.themes.THEME_DARK.copy(),
            )
            self._menuMain._disable_widget_update_mousepos_mouseselection = True

            self._menuMain.add.button('Play', self._menuPlay)
            self._menuMain.add.button('About', self._menuAbout)
            self._menuMain.add.button('Quit', pygame_menu.events.EXIT)


if __name__ == '__main__':
    DisplayGameOfLifeMenu()
