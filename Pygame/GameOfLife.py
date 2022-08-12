import numpy
import warnings
from os import PathLike
from settings import MAX_DAY_COUNT



class GameOfLife:

    # Play area
    array: numpy.ndarray
    rows: int
    cols: int
    infinityPlayArea: bool


    # Create new instance of GameOfLife with the given settings
    def __init__(self, array: numpy.ndarray, rows: int, cols: int, infinityPlayArea: bool = False):
        """
        Initializes a new GameOfLife instance with the given settings.
        :param array: The play area of the GameOfLife.
        :param rows: The number of rows in the play area.
        :param cols: The number of columns in the play area.
        :param infinityPlayArea: If true, the play area borders are connected.
        """
        if rows < 1 or cols < 1:
            raise ValueError("Invalid row or column count (must be greater than 0)")
        if array.shape != (rows, cols):
            raise ValueError("Invalid array shape (must be (rows, cols))")
        self.array = array
        self.rows = rows
        self.cols = cols
        self.infinityPlayArea = infinityPlayArea


    # Creates a new GameOfLife instance with the given settings
    @classmethod
    def fromSettings(cls, rows: int, cols: int, infinityPlayArea: bool = False):
        """
        Creates a new GameOfLife instance with the given settings.
        :param rows: The number of rows in the play area.
        :param cols: The number of columns in the play area.
        :param infinityPlayArea: If true, the play area borders are connected.
        :return: The new GameOfLife instance.
        """
        return cls(numpy.zeros((rows, cols)), rows, cols, infinityPlayArea)


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
        rows, cols = array.shape
        return cls(array, rows, cols, infinityPlayArea)

        
    def printToConsole(self):
        """
        Prints the current state of the GameOfLife to the console.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                print(self.array[row, col], end = " ")
            print()


    # Speichert Aktuellen Zustand in .npy Datei
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


    # borns a new cell at the given position
    def bornCell(self, x: int, y: int):
        """
        Borns a new cell at the given position.
        :param x: The x coordinate of the cell to born.
        :param y: The y coordinate of the cell to born.
        """
        if not 0 <= x < self.rows or not 0 <= y < self.cols:
            raise ValueError("Invalid cell position (0 <= x < {sef.rows}, 0 <= y < {sef.cols})")
        if self.array[x, y] == 0:
            self.array[x, y] =  1


    # kills a cell at the given position
    def killCell(self, x: int, y: int):
        """
        Kills a cell at the given position.
        :param x: The x coordinate of the cell to kill.
        :param y: The y coordinate of the cell to kill.
        """
        if not 0 <= x < self.rows or not 0 <= y < self.cols:
            raise ValueError("Invalid cell position (0 <= x < {sef.rows}, 0 <= y < {sef.cols})")
        self.array[x, y] = 0


    # toggels the cell at the given position
    def toggleCell(self, x: int, y: int):
        """
        Toggles live stat of a cell at the given position.
        :param x: The x coordinate of the cell to toggle.
        :param y: The y coordinate of the cell to toggle.
        """
        if not 0 <= x < self.rows or not 0 <= y < self.cols:
            raise ValueError("Invalid cell position (0 <= x < {sef.rows}, 0 <= y < {sef.cols})")
        self.array[x, y] = 1 if self.array[x, y] == 0 else 0


    # Get the number of live neighbors of the current cell
    def getLiveNeighbors(self, x: int, y: int):
        """
        Returns the number of live neighbors of the current cell.
        :param x: The x coordinate of the cell to get the live neighbors of.
        :param y: The y coordinate of the cell to get the live neighbors of.
        :return: The number of live neighbors of the current cell.
        """
        if not 0 <= x < self.rows or not 0 <= y < self.cols:
            raise ValueError("Invalid cell position (0 <= x < {sef.rows}, 0 <= y < {sef.cols})")
        # count the number of live neighbors
        liveNeighbors = 0
        if self.infinityPlayArea:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if self.array[(x + i) % self.rows, (y + j) % self.cols] >= 1:
                        liveNeighbors += 1
        else:
            for i in range(max(0, x - 1), min(self.rows, x + 2)):
                for j in range(max(0, y - 1), min(self.cols, y + 2)):
                    if self.array[i, j] >= 1:
                        liveNeighbors += 1

        if self.array[x, y] >= 1:
            liveNeighbors -= 1

        return liveNeighbors


    # cycles the GameOfLife one Day
    def cycleDay(self):
        """
        Cycles the GameOfLife one Day.
        """
        # Create a copy of the current state of the GameOfLife
        # This is necessary to avoid modifying the current state of the GameOfLife
        # while iterating over it.
        newDay = numpy.zeros(self.array.shape, dtype = int)
        # Iterate over the current state of the GameOfLife
        for row in range(self.rows):
            for col in range(self.cols):
                # Get the number of live neighbors of the current cell
                liveNeighbors = self.getLiveNeighbors(row, col)
                
                # Determine the new state of the current cell
                if self.array[row, col] >= 1:
                    if liveNeighbors == 2 or liveNeighbors == 3:
                        dayCount = self.array[row, col]
                        if dayCount < MAX_DAY_COUNT:
                            dayCount += 1
                        newDay[row, col] = dayCount
                    # else: newDay[row, col] = 0 no cange already set (default for newDay)
                else:
                    if liveNeighbors == 3:
                        newDay[row, col] = 1
                    # else: newDay[row, col] = 0 no cange already set (default for newDay)
        # Update the current state of the GameOfLife
        self.array = newDay
