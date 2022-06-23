import GameOfLife

gol = GameOfLife()
gol.loadFileData("Saves/10x10Glider.npy")
#gol.createNewArea(10,10)
gol.printToConsole()
#gol.saveFile("Saves/10x10Glider.npy")
for i in range(1,25):
    print(i)
    gol.cycleDay()
    gol.printToConsole()
    print()