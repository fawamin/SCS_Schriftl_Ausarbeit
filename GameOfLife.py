import pygame
import numpy


coldead = (0,0,0)
colalive = (255,255,255)

# 1 = alive
# 0 = dead

class GameOfLife:

    #Play area
    array = None
    #Filename of save file
    File = None

    def cycleDay(self):
        newDay = self.array.copy()
        rows, cols = self.array.shape
        for row, col in numpy.ndindex(self.array.shape):
            #Werte der nachbarn im array ermitteln
            # Nachbarwerte Ermitteln (Entrhält eigenen Wert)
            nachbar = self.array[max(row-1,0):min(row+2,rows), max(col-1,0):min(col+2,cols)]
            # Anzahl der lebenden Nachbarn ermitteln (Eigenen wert abziehen)
            amount_alive = nachbar.sum() - self.array[row,col]
            
            # Regeln für die nächste Generation
            if self.array[row,col] == 1:
                if amount_alive < 2 or amount_alive > 3:
                    newDay[row,col] = 0
                else:
                    newDay[row,col] = 1
            else:
                if amount_alive == 3:
                    newDay[row,col] = 1
                else:
                    newDay[row,col] = 0
        self.array = newDay
        
    def printToConsole(self):
        rows, cols = self.array.shape
        for row in range(rows):
            for col in range(cols):
                print(self.array[row,col], end = " ")
            print()

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
gol.loadFileData("Saves/5x5test.npy")
#gol.createNewArea(5,5)
gol.printToConsole()
for i in range(1,4):
    print(i)
    gol.cycleDay()
    gol.printToConsole()
    print()
#gol.saveFile("Saves/5x5test.npy")