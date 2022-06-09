import pygame
import numpy


coldead = (0,0,0)
colalive = (255,255,255)

def createandfill2darray(rows,columns):
    array = numpy.zeros((rows,columns))
    return array

def NextDay(surface,array,size):
    for row, column in numpy.ndindex(array.shape):
        pygame.draw.rect(surface, colalive , (row*size, column*size, size-1, size-1))


def main():
    ## Init
    pygame.init()
    windowsize = 750
    screen = pygame.display.set_mode((windowsize, windowsize))
    pygame.display.set_caption("Game of Life")
    clock = pygame.time.Clock()
    ## My code
    arraysize = 50
    array = createandfill2darray(arraysize,arraysize)
    squaresize = windowsize/arraysize
    NextDay(screen,array,squaresize)
    
    
    print(array)
    
    
    
    
    
    ## Main loop
    running = True
    while running:
        ## Stuff i did
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
    pygame.quit()
