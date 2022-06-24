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
    gol = None
    def __init__(self):
        self.gol = GameOfLife()
        self.gol.setSaveFile(File)

    def set_file(self,file):
        self.gol.setSaveFile = file
        
    def get_img(self):
        array = self.gol.getField()
        return Image.fromarray(np.uint8(array)*255,'L')

    def api_cycle(self):
        self.gol.cycleDay()

    # @TODO Add a function that gets all alive Cells in a Json
    def get_alive(self):
        storage ={}
        array = self.gol.getField
        for row,col in np.ndindex(self.array.shape):
            if array[row][col] == 1:
                storage.

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