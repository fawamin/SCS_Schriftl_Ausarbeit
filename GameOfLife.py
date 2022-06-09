from asyncio.windows_events import NULL
import pygame
import numpy


coldead = (0,0,0)
colalive = (255,255,255)
class GameOfLife:

    #Play area
    array = NULL
    #Size of play Area
    row = 0
    col = 0
    #Filename of save file
    File = NULL

    #def cycleDay(self):
    #    newDay = self.array.copy()
    #         for rows,cols in numpy.ndindex(self.array.shape):
    #       print(self.array[rows,cols])

    # Läd Daten aus .npy Speicherdatei
    def loadFileData(self, File):
        self.File = File
        self.array = numpy.load(self.File)
        self.row, self.col = self.array.shape

    # Speichert Aktuellen Zustand in .npy Datei
    def saveFile(self, File):
        self.File = File
        numpy.save(self.File, self.array)

    # Returns play Area
    def getField(self):
        return self.array

    # Erstellt neues Spielfeld mit den angegebenen Dimensionen
    def createNewArea(self, row,col):
        self.row = row
        self.col = col
        self.array = numpy.zeros((row,col), dtype=int)
        


gol = GameOfLife()
gol.loadFileData("Saves/test.npy")
gol.cycleDay()