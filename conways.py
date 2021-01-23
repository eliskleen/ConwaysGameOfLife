# from graphics import gameOfLifeGraphics
from os import times
import sys, pygame
from pygame.constants import MOUSEBUTTONUP
from pygame.display import update
from pygame.draw import line
from gameGraphics import gameOfLifeGraphics

pygame.init()
squares=100
squareSize=10
running = False
clock = pygame.time.Clock()
squareArray = [[False for x in range(squares)] for y in range(squares)]
framerate = 10
borders = False
rightButtonDown = False


def saveField(x1, y1, x2, y2):
    startX = min(x1, x2)
    startY = min(y1, y2)
    lines = []
    line = ""
    for x in range(abs(x1-x2)+1):
        for y in range(abs(y1-y2) +1):
            if graphics.squareArray[startX+x][startY + y]:
                line += "1"
            else:
                line += "0"
        line += "\n"
    graphics.saveFile(line)

def loadFile(x, y):
    try:
        txt = graphics.openFileDialog()
        lines = txt.splitlines()
        height = len(lines)
        width = len(lines[0])
        for i in range(height): 
            for j in range(width):
                line = lines[i]
                graphics.squareArray[(i+x) % squares][(j+y) % squares] = (line[j] == "1")
    except:
        pass
def updateGame():
    graphics.updateLife()
    graphics.drawSquares()
    update()

if __name__ == "__main__":
    lastFrame = 0
    black = 0, 0, 0
    white = 255, 255, 255
    windowSize = squares*squareSize + squares
    size = width, height = windowSize+1, windowSize+1
    screen = pygame.display.set_mode(size)
    global graphics
    graphics = gameOfLifeGraphics(screen, squares, squareSize, borders)

    graphics.drawField(black)
    graphics.drawSquares()
    rightMBDown = False
    squareToSave = [0, 0, 0, 0]

    while 1:
        # graphics.drawSquares()
        
        update()
        t = pygame.time.get_ticks()
        dt = t-lastFrame
        if dt > (1/framerate)*1000:
            lastFrame = t
            if running:
                graphics.white = 255, 255, 255
                updateGame()
            else:
                graphics.white = 128, 128, 128

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(pygame.mouse.get_pressed()[0]):
                    pos = pygame.mouse.get_pos()
                    graphics.changeSquareInPos(pos)
                    graphics.drawSquares()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_r:
                    running = not running 
                if event.key == pygame.K_a:
                    pos = pygame.mouse.get_pos()
                    (x,y) = graphics.getCordsInArray(pos)
                    alive = graphics.aliveAround(x, y)
                    print(alive)
                if event.key == pygame.K_s:
                    saveField(0, 0, squares, squares)
                if event.key == pygame.K_b:
                    graphics.borders = not graphics.borders
                    if graphics.borders: graphics.drawField(white)
                    else: graphics.drawField(black)
                if event.key == pygame.K_c:
                   graphics.squareArray = [[False for x in range(squares)] for y in range(squares)] 
            if(pygame.mouse.get_pressed()[2]):
                    try:
                        _ = event.pos
                        (x, y) = graphics.getCordsInArray(pygame.mouse.get_pos())
                        if not rightMBDown:
                            squareToSave[0] = x
                            squareToSave[1] = y
                        if rightMBDown:
                            graphics.drawSquares()
                            graphics.drawSquare(squareToSave[0], squareToSave[1], x, y)
                            squareToSave[2] = x
                            squareToSave[3] = y
                        rightMBDown = True
                    except AttributeError:
                        rightMBDown = False
                        graphics.drawSquares()
            else:
                if rightMBDown:
                    if squareToSave[0] > squareToSave[2]:
                        tmp = squareToSave[0]
                        squareToSave[0] = squareToSave[2]
                        squareToSave[3] = tmp
                    if squareToSave[1] > squareToSave[2]:
                        tmp = squareToSave[1]
                        squareToSave[1] = squareToSave[3]
                        squareToSave[3] = tmp
                    saveField(squareToSave[0]+1, squareToSave[1]-1, squareToSave[2]+1, squareToSave[3]-1)
                rightMBDown = False
                graphics.drawSquares()
            if pygame.mouse.get_pressed()[1]:
                (x,y) = graphics.getCordsInArray(pygame.mouse.get_pos())
                loadFile(x, y)
                graphics.drawSquares()

                        # squareToSave = [None, None, None, None]
    
class SquareToSave:
    start = (None, None)
    end = (None, None)