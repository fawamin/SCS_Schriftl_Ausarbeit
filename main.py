from GameOfLife import GameOfLife

saveFiles = [
    "Saves/3x3.npy",
    "Saves/5x5test.npy",
    "Saves/10x10Glider.npy",
    "Saves/64x64.npy",
    "Saves/test.npy"]

gol = GameOfLife()
gol.setSaveFile(saveFiles[1])
gol.loadFileData()
#gol.createNewArea(10,10)
gol.printToConsole()
#gol.saveFile("Saves/10x10Glider.npy")
for i in range(1,5):
    print(i)
    gol.cycleDay()
    gol.printToConsole()
    print()