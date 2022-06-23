import numpy


coldead = (0,0,0)
colalive = (255,255,255)

# 1 = alive
# 0 = dead
# test

class GameOfLife:

    #Play area
    array = None
    #Filename of save file
    File = None

    def cycleDay(self):
        newDay = self.array.copy()
        rows, cols = self.array.shape
        for row, col in numpy.ndindex(self.array.shape):
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
    def loadFileData(self):
        self.array = numpy.load(self.File)
        #self.row, self.col = self.array.shape

    #Sets the Save Filename  
    def setSaveFile(self,filename):
        self.File = filename

    # Speichert Aktuellen Zustand in .npy Datei
    def saveFile(self):
        numpy.save(self.File, self.array)

    # Returns play Area
    def getField(self):
        return self.array

    # Erstellt neues Spielfeld mit den angegebenen Dimensionen
    def createNewArea(self, row,col):
        self.row = row
        self.col = col
        self.array = numpy.zeros((row,col), dtype=int)

    #Changes the selected Cell at the Position X and Y between alive and dead
    def updateCell(self,cellX,cellY):
        try:
            isalive = self.array[cellX,cellY]
            if isalive == 0:
                self.array[cellX,cellY] = 1
            elif isalive == 1:
                self.array[cellX,cellY] = 0
        except:
            print("Position " + str(cellX) + " " + str(cellY) + " Is out of the Array Range") 