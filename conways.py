import sys, pygame
import time
from pygame.constants import MOUSEBUTTONUP

from pygame.display import update
from pygame.draw import line
pygame.init()
squares=50
squareSize=20
running = False
clock = pygame.time.Clock()
squareArray = [[False for x in range(squares)] for y in range(squares)]
framerate = 10
borders = True
def drawField(col):
    x = 0
    y = 0
    for _ in range(squares+1):
        start = (x,0)
        end   = (x, height)
        pygame.draw.line(screen, col, start, end, 1)
        start = (0, y)
        end   = (width, y)
        pygame.draw.line(screen, col, start, end, 1)
        x += (squareSize + 1)
        y += (squareSize + 1)
 
def fillSquare(x, y, col):
    left = x*(squareSize + 1) + 1
    top  = y*(squareSize + 1) + 1
    if not borders:
        rect = pygame.Rect(left, top, squareSize+1, squareSize+1)
    else:
        rect = pygame.Rect(left, top, squareSize, squareSize)
    pygame.draw.rect(screen, col, rect)

def changeSquareInPos(pos):
    x, y = pos
    x = int(x/(squareSize+1))
    y = int(y/(squareSize+1))
    if squareArray[x][y]:
        squareArray[x][y] = False
    else:
        (squareArray[x][y]) = True
    
def aliveAround(x, y):
    count = 0
    for i in range(-1, 2):      #y
        for j in range(-1, 2):  #x
            if i == 0 and j == 0:
                pass
            else:
                if squareArray[(x+j)%squares][(y+i)%squares]:
                    count += 1
    return count

def inside(x, y):
    if x < 0 or x >= squares or y < 0 or y >= squares:
        return False
    else:
        return True

def getCordsInArray(pos):
    x, y = pos
    x = int(x/(squareSize+1))
    y = int(y/(squareSize+1))
    return (x,y)

def isAlive(x, y):
    count = aliveAround(x, y) 
    selfAlive = squareArray[x][y]
    if selfAlive:
        if count >= 2 and count <= 3:
            return True
        else:
            return False
    else:
        if count == 3:
            return True
        else:
            return False

def updateLife():
    new = [[False for x in range(squares)] for y in range(squares)]
    for i in range(squares):
        for j in range(squares):
            new[i][j]=isAlive(i,j)
    for i in range(squares):
        for j in range(squares):
            squareArray[i][j] = new[i][j]
        

def drawSquares():
       for i in range(squares):
        for j in range (squares):
            if squareArray[i][j]:
                fillSquare(i, j, white)
            else:
                fillSquare(i, j, black)

def updateGame():
    updateLife()
    drawSquares()
    update()


def saveField():
    lines = []
    line = ""
    for i in range(squares):
        for j in range(squares):
            if squareArray[i][j]:
                line += "1"
            else:
                line += "0"
        line += "\n"

    f = open("savedFiles\\NewSave.txt", "w")
    f.write(line)

def loadFile(fileName):
    f = open(fileName, "r")
    txt = f.read()
    lines = txt.splitlines()
    squares = len(lines)
    array = [[False for x in range(squares)] for y in range(squares)] 
    for i in range(squares): 
        for j in range(squares):
            line = lines[i]
            array[i][j] = (line[j] == "1")
    return array
            

    


if __name__ == "__main__":
    try:
        file = sys.argv[1]
        print(file)
        squareArray = loadFile(file)
    except:
        squareArray = [[False for x in range(squares)] for y in range(squares)]
    lastFrame = 0
    black = 0, 0, 0
    white = 255, 255, 255
    windowSize=squares*squareSize + squares
    size = width, height = windowSize+1, windowSize+1 
    screen = pygame.display.set_mode(size)
    drawField(black)
    drawSquares()
    while 1:
        drawSquares()
        update()
        t = pygame.time.get_ticks()
        dt = t-lastFrame
        if dt > (1/framerate)*1000:
            lastFrame = t
            if running:
                updateGame()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: sys.exit()
            if event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                changeSquareInPos(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_r:
                    running = not running 

                if event.key == pygame.K_a:
                    pos = pygame.mouse.get_pos()
                    (x,y) = getCordsInArray(pos)
                    alive = aliveAround(x, y)
                    print(alive)
                if event.key == pygame.K_s:
                    saveField()
                if event.key == pygame.K_b:
                    borders = not borders
                    if borders: drawField(white)
                    else: drawField(black)
                if event.key == pygame.K_c:
                   squareArray = [[False for x in range(squares)] for y in range(squares)] 
    
