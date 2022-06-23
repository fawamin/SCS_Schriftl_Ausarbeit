from GameOfLife import GameOfLife

gol = GameOfLife()
gol.setSaveFile("Saves/5x5test.npy")
gol.loadFileData()
#gol.createNewArea(10,10)
gol.printToConsole()
#gol.saveFile("Saves/10x10Glider.npy")
for i in range(1,5):
    print(i)
    gol.cycleDay()
    gol.printToConsole()
    print()