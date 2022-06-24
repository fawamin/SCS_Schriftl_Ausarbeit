from matplotlib.font_manager import json_dump
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from GameOfLife import GameOfLife

#array = np.load("Saves/10x10Glider.npy")
#x,y = array.shape
#img = Image.fromarray(np.uint8(array)*255,'L')
#img.show()

class Api:

    #GOL_instance  = None

    def __init__(self):
        self.GOL_instance = GameOfLife()
        print(self.GOL_instance.getField)

    def init_file(self,file):
        self.GOL_instance.setSaveFile(file)
        self.GOL_instance.loadFileData()
        
    # Returns a List representation of the Game of Life Board 
    def get_array(self):
        return self.GOL_instance.getField().tolist()

    def api_cycle(self):
        self.GOL_instance.cycleDay()

    # @TODO Add a function that gets all alive Cells in a Json
    def get_alive(self):
        storage ={}
        array = self.GOL_instance.getField
        for row,col in np.ndindex(self.array.shape):
            if array[row][col] == 1:
                pass

#img = Image.new('1', (x,y))
#pixel = img.load()
#for i in range(x):
#    for j in range(y):
#        pixel[i,j] = array[i][j]
#
#img.show()
#plt.figure()
#plt.imshow(array,interpolation='none')
#plt.show()