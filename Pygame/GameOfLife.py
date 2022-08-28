import numpy
import warnings
from os import PathLike
from Settings import MAX_DAY_COUNT



class GameOfLife:

    #Set that contains all living cell positions
    livingCells: set()
    #Playarea that Contains Cells and Cell Age
    array: numpy.ndarray
    cols: int
    rows: int
    infinityPlayArea: bool


    # Create new instance of GameOfLife with the given settings
    def __init__(self, array: numpy.ndarray, cols: int, rows: int, livingCells: set() ,infinityPlayArea: bool = False):
        """
        Initializes a new GameOfLife instance with the given settings.
        :param array: The play area of the GameOfLife.
        :param cols: The number of columns in the play area.
        :param rows: The number of rows in the play area.
        :param infinityPlayArea: If true, the play area borders are connected.
        """
        if cols < 1 or rows < 1:
            raise ValueError("Invalid row or column count (must be greater than 0)")
        if array.shape != (cols, rows):
            raise ValueError("Invalid array shape (must be (rows, cols))")
        self.array = array
        self.cols = cols
        self.rows = rows
        self.infinityPlayArea = infinityPlayArea
        self.livingCells = livingCells


    # Creates a new GameOfLife instance with the given settings
    @classmethod
    def fromSettings(cls, cols: int, rows: int, infinityPlayArea: bool = False):
        """
        Creates a new GameOfLife instance with the given settings.
        :param cols: The number of columns in the play area.
        :param rows: The number of rows in the play area.
        :param infinityPlayArea: If true, the play area borders are connected.
        :return: The new GameOfLife instance.
        """
        return cls(numpy.zeros((cols, rows), dtype = int), cols, rows, set(), infinityPlayArea,)

    # Creates a new GameOfLife Instance from loaded File
    @classmethod
    def fromFile(cls, loadFileName: str | bytes | PathLike[str], infinityPlayArea: bool = False):
        """
        Initializes a new GameOfLife instance from a saved area.
        :param loadFileName: The name of the file to load the play area from.
        :param infinityPlayArea: If true, the play area borders are connected.
        :return: The new GameOfLife instance.
        """
        try:
            array: numpy.ndarray = numpy.load(loadFileName)
        except Exception as e:
            raise ValueError("Could not load file: \n" + str(e))
        cols, rows = array.shape
        cells = set()
        for row in range(rows):
            for col in range(cols):
                if array[col,row] >= 1:
                    cells.add((col,row))
        return cls(array, cols, rows, cells, infinityPlayArea)

    #Prints the GameOfLife Playboard to the Console
    def printToConsole(self):
        """
        Prints the current state of the GameOfLife to the console.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                print(self.array[col, row], end = " ")
            print()


    # Saves the current Playboard to a .npy File
    def saveFile(self, saveFileName: str | PathLike[str]):
        """
        Saves the current state of the GameOfLife to a file.
        :param saveFileName: The name of the file to save the play area to.
        """
        try:
            numpy.save(saveFileName, self.array)
        except Exception as e:
            # ("Could not save file: \n" + str(e))
            warnings.warn("Could not save file: \n" + str(e), ResourceWarning)


    # Returns play Area
    def getField(self):
        """
        Returns the play area of the GameOfLife.
        :return: The play area of the GameOfLife.
        """
        return self.array.copy()

    # Returns living Cell set
    def getlivingCells(self):
        """
        Returns currently living Cellpositions
        :return: Set of Living cells
        """
        return self.livingCells.copy()

    # birth a new cell at the given position
    def birthCell(self, x: int, y: int):
        """
        Creates a new cell at the given position.
        :param x: The x coordinate of the cell to be created.
        :param y: The y coordinate of the cell to be created.
        """
        if not 0 <= x < self.cols or not 0 <= y < self.rows:
            raise ValueError("Invalid cell position (0 <= x < {sef.cols}, 0 <= y < {self.rows})")
        if self.array[x, y] == 0:
            self.array[x, y] =  1
        self.livingCells.add((x, y))


    # kills the cell at the given position
    def killCell(self, x: int, y: int):
        """
        Kills the cell at the given position.
        :param x: The x coordinate of the cell to kill.
        :param y: The y coordinate of the cell to kill.
        """
        if not 0 <= x < self.cols or not 0 <= y < self.rows:
            raise ValueError("Invalid cell position (0 <= x < {sef.cols}, 0 <= y < {self.rows})")
        self.array[x, y] = 0
        if (x, y) in self.livingCells:
            self.livingCells.remove((x, y))
        


    # toggles the cell at the given position
    def toggleCell(self, x: int, y: int):
        """
        Toggles live stat of a cell at the given position.
        :param x: The x coordinate of the cell to toggle.
        :param y: The y coordinate of the cell to toggle.
        """
        if not 0 <= x < self.cols or not 0 <= y < self.rows:
            raise ValueError("Invalid cell position (0 <= x < {sef.cols}, 0 <= y < {self.rows})")
        if self.array[x, y] == 0:
            self.array[x, y] = 1
            self.livingCells.add((x, y))
        else:
            self.array[x, y] = 0
            self.livingCells.remove((x, y))

    # Get the number of living neighbors of the current cell
    def getLiveNeighbors(self, x: int, y: int):
        """
        Returns the number of live neighbors of the current cell.
        :param x: The x coordinate of the cell to get the live neighbors of.
        :param y: The y coordinate of the cell to get the live neighbors of.
        :return: The number of live neighbors of the current cell.
        """
        if not 0 <= x < self.cols or not 0 <= y < self.rows:
            raise ValueError("Invalid cell position (0 <= x < {sef.cols}, 0 <= y < {self.rows})")
        # count the number of live neighbors
        liveNeighbors = 0
        if self.infinityPlayArea:
            for i in [-1, 0, 1]:
                row = (y + i) % self.rows
                for j in [-1, 0, 1]:
                    col = (x + j) % self.cols
                    if self.array[col, row] >= 1:
                        liveNeighbors += 1
        else:
            for i in range(max(0, y - 1), min(self.rows, y + 2)):
                for j in range(max(0, x - 1), min(self.cols, x + 2)):
                    if self.array[j, i] >= 1:
                        liveNeighbors += 1

        if self.array[x, y] >= 1:
            liveNeighbors -= 1

        return liveNeighbors

    def InfinityEnabled(self):
        """
        Creates List of Cells that have at least 1 living neighbor Cell including over and underflow of coordinates
        :return: List of Cells
        """
        potentialCells = set()
        for x,y in self.livingCells:
            for i in [-1, 0, 1]:
                row = (y + i) % self.rows
                for j in [-1, 0, 1]:
                    col = (x + j) % self.cols
                    potentialCells.add((col, row))     
        return potentialCells


    def InfinityDisabled(self):
        """
        Creates List of Cells that have at least 1 living neighbor Cell excluding over and underflow of coordinates
        :return: List of Cells
        """
        potentialCells = set()
        for x,y in self.livingCells:
            for row in range(max(0, y - 1), min(self.rows, y + 2)):
                for col in range(max(0, x - 1), min(self.cols, x + 2)): 
                    potentialCells.add((col, row))
        return potentialCells

    def cycleDay(self):
        """
        Cycles To the Next Day
        """
        #Is there a Cell alive
        if len(self.livingCells) != 0:
            #Find Potential Cells Depending on Game setting
            if self.infinityPlayArea:
                potentialCells = self.InfinityEnabled()
            else:
                potentialCells = self.InfinityDisabled()
            #Set of new Living Cells
            living = set()
            #Array of next Day
            newDay = numpy.zeros(self.array.shape, dtype = int)
            #Go through all Cells that might live
            for col,row in potentialCells:
                #Calculate Neigbors
                liveNeighbors = self.getLiveNeighbors(col, row)
                if self.array[col, row] >= 1:
                    if liveNeighbors == 2 or liveNeighbors == 3:
                        dayCount = self.array[col, row]
                        if dayCount < MAX_DAY_COUNT:
                            dayCount += 1
                        newDay[col, row] = dayCount
                        living.add((col, row))
                else:
                    if liveNeighbors == 3:
                        newDay[col, row] = 1
                        living.add((col, row))
            #Overwrite old day with new Day
            self.array = newDay
            self.livingCells = living