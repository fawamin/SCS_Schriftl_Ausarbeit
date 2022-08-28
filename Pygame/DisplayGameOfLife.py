import Settings
import pygame
import pygame_menu
import pygame_menu.widgets
import pygame_menu.themes
import pygame_menu.events
import pygame_menu.locals

import os
from GameOfLife import GameOfLife


class DisplayGameOfLife:

    # object variables
    _screen: pygame.Surface
    _cols: int
    _rows: int
    _infinityPlayArea: bool
    _cellSize: int
    _cellMargin: int
    _cellBorderRadius: int
    _cellHoverSize: int
    _cellHoverMargin: int
    _menuMain: pygame_menu.Menu | None
    _gameStarted: bool
    _valuesSet: bool
    _dayCycleEvent: pygame.event.Event
    _dayCyclePlay : bool
    _dayCycleSpeed: int
    _patternActive: bool
    _selectedPattern: list[list[int | None]]
    _currentPattern: list[list[int | None]]
    _gol: GameOfLife
    _playMenu: pygame_menu.Menu
    _drawSurface: pygame.Surface
    _playWidget: pygame_menu.widgets.SurfaceWidget
    _totalCellSize: int


    # initialize DisplayGOL
    def __init__(self, screen: pygame.Surface):
        # initialize pygame if not already initialized
        if not pygame.get_init():
            pygame.init()

        self._screen = screen
        self._gameStarted = False
        self._valuesSet = False
        self._dayCycleEvent = pygame.event.Event(pygame.USEREVENT)


    # start new game
    def startGameFromSettings(self, cols: int, rows: int, infinityPlayArea: bool, cellSize: int, cellMargin: int, cellBorderRadius: int, cellHoverBorderWidth: int,  menuMain: pygame_menu.Menu | None = None):
        # check if game is already started
        if self._gameStarted:
            raise Exception("Game is already started")

        # set game started to true
        self._gameStarted = True

        # check if cols and rows are valid
        if cols < 1 or rows < 1:
            raise ValueError("Invalid column or row count (must be greater than 0)")

        # create new game of life
        self._gol = GameOfLife.fromSettings(cols, rows, infinityPlayArea)

        # create play menu
        self._startGame(cols, rows, infinityPlayArea, cellSize, cellMargin, cellBorderRadius, cellHoverBorderWidth, menuMain)


    # start game from File
    def startGameFromFile(self, fileName: str | bytes | os.PathLike[str], infinityPlayArea: bool, cellSize: int, cellMargin: int, cellBorderRadius: int, cellHoverBorderWidth: int,  menuMain: pygame_menu.Menu | None = None):
        # check if game is already started
        if self._gameStarted:
            raise Exception("Game is already started")

        # set game started to true
        self._gameStarted = True

        # create new game of life
        self._gol = GameOfLife.fromFile(fileName, infinityPlayArea)
        # set cols and rows to size of loaded field
        cols, rows = self._gol.getField().shape

        # create play menu
        self._startGame(cols, rows, infinityPlayArea, cellSize, cellMargin, cellBorderRadius, cellHoverBorderWidth, menuMain)


    # create play menu
    def _startGame(self, cols:int, rows: int, infinityPlayArea: bool, cellSize: int, cellMargin: int, cellBorderRadius: int, cellHoverBorderWidth: int,  menuMain: pygame_menu.Menu | None = None):
        # check if game is already started
        if not self._gameStarted:
            raise Exception("Game is not started")

        # check if values are set
        if self._valuesSet:
            raise Exception("Values are already set")

        # check if cols and rows are valid
        if cols < 1 or rows < 1:
            raise ValueError("Invalid column or row count (must be greater than 0)")

        # check if cellSize is valid
        if cellSize < 1:
            raise ValueError("Invalid cell size (must be greater than 0)")

        # check if cellMargin is valid
        if cellMargin < 0:
            raise ValueError("Invalid cell margin (must be greater than or equal to 0)")

        # check if cellBorderRadius is valid
        if cellBorderRadius < 0:
            raise ValueError("Invalid cell border radius (must be greater than or equal to 0)")

        # check if cellHoverBorderWidth is valid
        if cellHoverBorderWidth < 0 or cellHoverBorderWidth * 2 >= cellSize:
            raise ValueError("Invalid cell hover border width (must be greater than or equal to 0 and less than half the cell size)")

        # set values set to true
        self._valuesSet = True

        # set variables
        self._cols = cols
        self._rows = rows
        self._infinityPlayArea = infinityPlayArea
        self._cellSize = cellSize
        self._cellMargin = cellMargin
        self._cellBorderRadius = cellBorderRadius
        self._cellSpaceMargin = cellMargin + cellHoverBorderWidth
        self._cellSpaceSize = cellSize - cellHoverBorderWidth * 2
        self._cellHoverMargin = cellMargin + cellHoverBorderWidth * 2
        self._cellHoverSize = cellSize - cellHoverBorderWidth * 4
        self._totalCellSize = cellSize + cellMargin * 2
        self._menuMain = menuMain

        # disable main menu if set
        if self._menuMain is not None:
            self._menuMain.disable()

        # create play menu
        self._playMenu = pygame_menu.Menu(
            Settings.TITLE_BASE,
            self._screen.get_width(),
            self._screen.get_height(),
            False,
            theme = pygame_menu.themes.THEME_DARK.copy(),
            columns = 3,
            rows = [1, 12, 2],
        )
        self._playMenu._disable_widget_update_mousepos_mouseselection = True
        self._playMenu.add.horizontal_margin(10)


        self._playMenu.add.vertical_margin(15)
        self._playMenu.add.button("Cycle Day", pygame.event.post,self._dayCycleEvent ,align = pygame_menu.locals.ALIGN_LEFT)
        self._playMenu.add.toggle_switch("Day Cycle:", state_text = ("Pause", "Play"), onchange = self._onDayCyclePause, align = pygame_menu.locals.ALIGN_LEFT)
        dayCycleSpeeds = [(speed, Settings.DAY_CYCLE_SPEEDS[speed]) for speed in Settings.DAY_CYCLE_SPEEDS]
        if len(dayCycleSpeeds) > 0:
            self._dayCycleSpeed = dayCycleSpeeds[0][1]
            self._playMenu.add.dropselect(
                "Day Cycle Speed:",
                dayCycleSpeeds,
                0,
                onchange = self._onDayCycleSpeedChange,
                placeholder_add_to_selection_box = False,
                selection_box_width = 150,
                selection_box_height = 4,
                align = pygame_menu.locals.ALIGN_LEFT
            )
        else:
            self._dayCycleSpeed = 0
            self._playMenu.add.label("No Day Cycle Speeds set", align = pygame_menu.locals.ALIGN_LEFT)
        # pause Game on new start
        self._onDayCyclePause(False)

        self._playMenu.add.toggle_switch("Selection Type:", state_text = ("single", "pattern"), onchange = self._onSelectionTypeChange, align = pygame_menu.locals.ALIGN_LEFT)
        patterns =  []
        for pattern in Settings.PATTERNS:
            maxPatternHight = len(pattern)
            if maxPatternHight > self._rows:
                continue
            maxPatternWidth = 0
            for i in range(maxPatternHight):
                maxPatternWidth = max(maxPatternWidth, len(pattern[i]))
            if maxPatternWidth > self._cols:
                continue
            patterns.append((pattern, Settings.PATTERNS[pattern]))

        if len(patterns) > 0:
            self._selectedPattern = patterns[0][1]
            self._playMenu.add.dropselect(
                "Pattern:",
                patterns,
                0,
                onchange = self._onPatternChange,
                placeholder_add_to_selection_box = False,
                selection_box_width = 150,
                selection_box_height = 4,
                align = pygame_menu.locals.ALIGN_LEFT
            )
        else:
            self._selectedPattern = [[1]]
            self._playMenu.add.label("No Patterns big enough for selected size", align = pygame_menu.locals.ALIGN_LEFT)
        # reset pattern Type on new start
        self._onSelectionTypeChange(False)

        # add option to save playfield to file
        if os.path.isdir(Settings.DIR_SAVE):
            self._playMenu.add.toggle_switch("allow overwrite:", state_text = ("No", "Yes"), align = pygame_menu.locals.ALIGN_LEFT, toggleswitch_id="overwrite")
            self._playMenu.add.text_input("Filename: ", align = pygame_menu.locals.ALIGN_LEFT, textinput_id="saveFileName", input_underline="_", input_underline_len=15)
            self._playMenu.add.button("Save Game", self._onSavePlayfield, align = pygame_menu.locals.ALIGN_LEFT)
        else:
            self._playMenu.add.none_widget()
            self._playMenu.add.label("Save directory not found", align = pygame_menu.locals.ALIGN_LEFT)
            self._playMenu.add.none_widget()

        self._playMenu.add.vertical_fill()
        self._playMenu.add.button("Return to Main Menu", self.exit, align = pygame_menu.locals.ALIGN_LEFT)
        self._playMenu.add.button("Quit", pygame_menu.events.EXIT, align = pygame_menu.locals.ALIGN_LEFT)
        self._playMenu.add.vertical_margin(10)


        # create draw Surface
        self._drawSurface = pygame.Surface(size = (self._cols * self._totalCellSize, self._rows * self._totalCellSize))
        self._drawSurface.fill(Settings.COLOR_PLAY_SURFACE_BACKGROUND)
        self._drawSurface.set_colorkey(Settings.COLOR_PLAY_SURFACE_COLORKEY)

        # create play Surface
        self.playSurface = pygame.Surface(size = self._drawSurface.get_size())

        # add play surface to play menu
        self._playWidget = self._playMenu.add.surface(
            self._drawSurface,
            "playWidget",
            selectable = True,
            selection_effect = pygame_menu.widgets.NoneSelection(),
            align = pygame_menu.locals.ALIGN_LEFT
        )

        self._renderPlaySurface(renderAll = True)


    # is enabled
    def is_enabled(self):
        return self._gameStarted and self._valuesSet and self._playMenu.is_enabled()


    # update events
    def update(self, events: list[pygame.event.Event]):
        # check if instance is enabled#
        if not self.is_enabled():
            raise Exception("Instance is not enabled")

        # if crtl is pressed ignore cells to kill
        ctrlPressd = True if pygame.key.get_mods() & pygame.KMOD_CTRL else False
        updatedCells = set()

        for event in events:
            if event.type == self._dayCycleEvent.type:
                # cicle day and render play surface
                updatedCells.update(self._gol.cycleDay())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #Pattern active or not
                    if self._patternActive:
                        updatedCells.update(self._setPattern(self._currentPattern, ctrlPressd))
                    else:
                        updatedCells.update(self._toggleCell())
                elif event.button == 3:
                    # set pattern invert patter
                    updatedCells.update(self._setPattern(self._currentPattern, ctrlPressd, True))

        if len(updatedCells) > 0:
            self._renderPlaySurface(updatedCells)

        self._drawSurface.blit(self.playSurface, (0, 0))
        self._previewPattern(self._currentPattern, ctrlPressd)
        self._playWidget.force_menu_surface_update()

        self._playMenu.update(events)

    # draw
    def draw(self):
        # check if instance is enabled
        if not self.is_enabled():
            raise Exception("Instance is not enabled")

        # draw play menu
        self._playMenu.draw(self._screen)


    # resize
    def resize(self, width: int, height: int):
        if self._gameStarted and self._valuesSet:
            self._playMenu.resize(width, height)


    # exit
    def exit(self):
        # check if game is not started
        if not self._gameStarted:
            raise Exception("Game is not started")

        # check if values are not set
        if not self._valuesSet:
            raise Exception("Values are not set")

        # disable play menu
        self._playMenu.disable()

        # enable main menu
        if self._menuMain is not None:
            self._menuMain.enable()
            self._menuMain.full_reset()

        # set game started to false
        self._gameStarted = False

        # set play menu created to false
        self._valuesSet = False


    # on day cycle pause
    def _onDayCyclePause(self,  play: bool):
        speed = 0
        if play:
            speed = self._dayCycleSpeed
        pygame.time.set_timer(self._dayCycleEvent.type, speed)
        self._dayCyclePlay = play


    # on day cycle speed change
    def _onDayCycleSpeedChange(self, selectedItemIndex, *kwargs):
        # check if game is not started
        if not self._gameStarted:
            raise Exception("Game is not started")
        # check if values are not set
        if not self._valuesSet:
            raise Exception("Values are not set")
        speed = selectedItemIndex[0][1]
        # set time for day cycle event if day cycle is play
        if self._dayCyclePlay:
            pygame.time.set_timer(self._dayCycleEvent.type, speed)
        self._dayCycleSpeed = speed


    # on selection type change
    def _onSelectionTypeChange(self, patternsActive: bool):
        if patternsActive:
            self._currentPattern = self._selectedPattern
        else:
            self._currentPattern = [[1]]
        self._patternActive = patternsActive


    # on pattern change
    def _onPatternChange(self, selectedItemIndex, *kwargs):
        self._selectedPattern = selectedItemIndex[0][1]
        if self._patternActive:
            self._currentPattern = self._selectedPattern


    # save playfield
    def _onSavePlayfield(self, *kwargs):
        # check if game is not started
        if not self._gameStarted:
            raise Exception("Game is not started")
        # check if values are not set
        if not self._valuesSet:
            raise Exception("Values are not set")
        # check if save directory is not found
        if not os.path.isdir(Settings.DIR_SAVE):
            return
        # get save file name
        saveFileName = self._playMenu.get_widget("saveFileName").get_value()
        # check if save file name is not empty
        if saveFileName == "":
            return
        saveFilePath = os.path.join(Settings.DIR_SAVE, saveFileName)
        if saveFilePath.endswith(".npy"):
            saveFilePath = saveFilePath[:-4]
        # check if save file name is not in use
        if os.path.exists(saveFilePath + ".npy") and not self._playMenu.get_widget("overwrite").get_value():
            return
        # save playfield to file
        self._gol.saveFile(saveFilePath)


    # render play surface
    def _renderPlaySurface(self, updatedCells: set[tuple[int, int]] = set(), renderAll: bool = False):
        # check if game is not started
        if not self._gameStarted:
            raise Exception("Game is not started")

        # check if values are not set
        if not self._valuesSet:
            raise Exception("Values are not set")

        # get field
        field = self._gol.getField()

        if renderAll:
            # clear play surface
            self.playSurface.fill(Settings.COLOR_PLAY_SURFACE_BACKGROUND)
            self.playSurface.set_colorkey(Settings.COLOR_PLAY_SURFACE_COLORKEY)
            # self.playSurface.set_alpha(255)

            # draw cells
            for row in range(self._rows):
                y = row * self._totalCellSize + self._cellMargin
                for col in range(self._cols):
                    x = col * self._totalCellSize + self._cellMargin
                    # set cell colour
                    cellDay = field[col, row]
                    color = None
                    # get cell colour from highest minimum day
                    for gen in Settings.COLOR_CELL:
                        if cellDay >= Settings.COLOR_CELL[gen]["MIN_DAYS"]:
                            color = Settings.COLOR_CELL[gen]["COLOR"]
                        else:
                            break
                    # check if colour is set
                    if color is None:
                        raise Exception("No colour found for cell day " + str(cellDay))

                    # draw cell
                    pygame.draw.rect(
                        self.playSurface,
                        color,
                        (x, y, self._cellSize, self._cellSize),
                        border_radius = self._cellBorderRadius
                    )
        else:
            # draw cell updates
            for col, row in updatedCells:
                y = row * self._totalCellSize + self._cellMargin
                x = col * self._totalCellSize + self._cellMargin
                # set cell colour
                cellDay = field[col, row]
                color = None
                # get cell colour from highest minimum day
                for gen in Settings.COLOR_CELL:
                    if cellDay >= Settings.COLOR_CELL[gen]["MIN_DAYS"]:
                        color = Settings.COLOR_CELL[gen]["COLOR"]
                    else:
                        break
                # check if colour is set
                if color is None:
                    raise Exception("No colour found for cell day " + str(cellDay))

                # draw cell
                pygame.draw.rect(
                    self.playSurface,
                    color,
                    (x, y, self._cellSize, self._cellSize),
                    border_radius = self._cellBorderRadius
                )


    # calculate index from mouse position
    def _calculateIndex(self):
        # check if game is not started
        if not self._gameStarted:
            raise Exception("Game is not started")

        # check if values are not set
        if not self._valuesSet:
            raise Exception("Values are not set")

        # get mouse position
        mouseX, mouseY = pygame.mouse.get_pos()
        # get inner scroll area size
        scrollAreaSIzeX, scrollAreaSIzeY = self._playMenu.get_scrollarea().get_size(True)

        # check if mouse is over scroll area
        if mouseX >= scrollAreaSIzeX or mouseY >= scrollAreaSIzeY:
            return None

        # get play surface position
        playWidgetX, playWidgetY = self._playWidget.get_position()
        # get scroll area position
        scrollAreaOffsetsX, scrollAreaOffsetsY = self._playMenu.get_scrollarea().get_offsets()

        # calculate index
        indexX = (mouseX - playWidgetX + scrollAreaOffsetsX) // self._totalCellSize
        indexY = (mouseY - playWidgetY + scrollAreaOffsetsY) // self._totalCellSize

        # check if index is in range
        if indexX < 0 or indexX >= self._cols or indexY < 0 or indexY >= self._rows:
            return None
        else:
            return indexX, indexY


    # preview pattern
    def _previewPattern(self, pattern: list[list[int | None]], ignoreCellsToKill: bool = False):
        # check if game is not started
        if not self._gameStarted:
            raise Exception("Game is not started")

        # check if values are not set
        if not self._valuesSet:
            raise Exception("Values are not set")

        maxPatternHight = len(pattern)
        maxPatternWidth = 0
        for i in range(maxPatternHight):
            maxPatternWidth = max(maxPatternWidth, len(pattern[i]))

        # check if pattern is valid
        if maxPatternWidth > self._cols or maxPatternHight > self._rows:
            raise Exception("Pattern is too big for play area")

        # get index from mouse position
        index = self._calculateIndex()

        if index is not None and not self._infinityPlayArea:
            # check if pattern is inside the play area
            if index[0] + maxPatternWidth > self._cols or index[1] + maxPatternHight > self._rows:
                index = None

        if index is not None:
            # draw preview cells
            previewSurface = pygame.Surface(self._drawSurface.get_size(), pygame.SRCALPHA)

            for i in range(len(pattern)):
                row = index[1] + i
                if self._infinityPlayArea:
                    row = row % self._rows
                y = row * self._totalCellSize + self._cellMargin
                hoverY = row * self._totalCellSize + self._cellHoverMargin
                spaceY = row * self._totalCellSize + self._cellSpaceMargin

                for j in range(len(pattern[i])):
                    if pattern[i][j] == None or pattern[i][j] < 0:
                        continue
                    elif pattern[i][j] == 0:
                        if ignoreCellsToKill:
                            continue
                        borderColor = (255, 0, 0, 255)
                    else: # > 0
                        borderColor = (0, 255, 0, 255)

                    col = index[0] + j
                    if self._infinityPlayArea:
                        col = col % self._cols
                    x = col * self._totalCellSize + self._cellMargin
                    hoverX = col * self._totalCellSize + self._cellHoverMargin
                    spaceX = col * self._totalCellSize + self._cellSpaceMargin

                    pygame.draw.rect(
                        previewSurface,
                        borderColor,
                        (x, y, self._cellSize, self._cellSize),
                        border_radius = self._cellBorderRadius
                    )
                    pygame.draw.rect(
                        previewSurface,
                        Settings.COLOR_PLAY_SURFACE_BACKGROUND,
                        (spaceX, spaceY, self._cellSpaceSize, self._cellSpaceSize),
                        border_radius = self._cellBorderRadius
                    )
                    pygame.draw.rect(
                        previewSurface,
                        (0, 0, 0, 0),
                        (hoverX, hoverY, self._cellHoverSize, self._cellHoverSize),
                        border_radius = self._cellBorderRadius
                    )
            self._drawSurface.blit(previewSurface, (0, 0))


    # set pattern
    def _setPattern(self, pattern: list[list[int | None]], ignoreCellsToKill: bool = False, invert: bool = False):
        # check if game is not started
        if not self._gameStarted:
            raise Exception("Game is not started")

        # check if values are not set
        if not self._valuesSet:
            raise Exception("Values are not set")

        maxPatternHight = len(pattern)
        maxPatternWidth = 0
        for i in range(maxPatternHight):
            maxPatternWidth = max(maxPatternWidth, len(pattern[i]))

        # check if pattern is valid
        if maxPatternWidth > self._cols or maxPatternHight > self._rows:
            raise Exception("Pattern is too big for play area")

        # get index from mouse position
        index = self._calculateIndex()

        if index is not None and not self._infinityPlayArea:
            # check if pattern is inside the play area
            if index[0] + maxPatternWidth > self._cols or index[1] + maxPatternHight > self._rows:
                index = None

        updatedCells = set()
        if index is not None:
            for i in range(len(pattern)):
                row = index[1] + i
                if self._infinityPlayArea:
                    row = row % self._rows
                for j in range(len(pattern[i])):
                    if pattern[i][j] == None or pattern[i][j] < 0:
                        continue
                    elif pattern[i][j] == 0:
                        if ignoreCellsToKill:
                            continue
                        killCell = True
                    else: # > 0
                        killCell = False

                    if invert:
                        killCell = not killCell

                    col = index[0] + j
                    if self._infinityPlayArea:
                        col = col % self._cols

                    if killCell:
                        self._gol.killCell(col, row)
                    else: # > 0
                        self._gol.birthCell(col, row)
                    updatedCells.add((col, row))
        return updatedCells


    #Toggles the Current Cell between alive and dead
    def _toggleCell(self):
        # check if game is not started
        if not self._gameStarted:
            raise Exception("Game is not started")

        # check if values are not set
        if not self._valuesSet:
            raise Exception("Values are not set")

        updatedCells = set()
        index = self._calculateIndex()
        if index is not None:
            self._gol.toggleCell(index[0], index[1])
            updatedCells.add(index)
        return updatedCells
