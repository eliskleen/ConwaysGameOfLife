import sys, pygame
from typing import Text
from pygame.constants import MOUSEBUTTONUP
from pygame.display import update
from pygame.draw import line
# import all components 
import os
# import filedialog module 
from tkinter import filedialog 
import tkinter

class gameOfLifeGraphics:
    screen = 0
    squares = 0
    squareSize = 0
    windowSize = 0
    width = 0
    height = 0
    borders = False
    squareArray = 0
    black = 0, 0, 0
    white = 255, 255, 255
    
    def __init__(self, screen, squares, squareSize, borders) -> None:
        self.screen = screen
        self.squares = squares
        self.squareSize = squareSize
        self.windowSize = squares*squareSize + squares
        self.size = self.width, self.height = self.windowSize+1, self.windowSize+1
        self.borders = borders
        self.squareArray = [[False for x in range(squares)] for y in range(squares)]
        
    def drawField(self, col):
        x = 0
        y = 0
        for _ in range(self.squares+1):
            start = (x,0)
            end   = (x, self.height)
            pygame.draw.line(self.screen, col, start, end, 1)
            start = (0, y)
            end   = (self.width, y)
            pygame.draw.line(self.screen, col, start, end, 1)
            x += (self.squareSize + 1)
            y += (self.squareSize + 1)
    
    def fillSquare(self, x, y, col):
        left = x*(self.squareSize + 1) + 1
        top  = y*(self.squareSize + 1) + 1
        if not self.borders:
            rect = pygame.Rect(left, top, self.squareSize+1, self.squareSize+1)
        else:
            rect = pygame.Rect(left, top, self.squareSize, self.squareSize)
        pygame.draw.rect(self.screen, col, rect)

    def changeSquareInPos(self, pos):
        x, y = pos
        x = int(x/(self.squareSize+1))
        y = int(y/(self.squareSize+1))
        if self.squareArray[x][y]:
           self.squareArray[x][y] = False
        else:
            (self.squareArray[x][y]) = True

    def aliveAround(self, x, y):
        count = 0
        for i in range(-1, 2):      #y
            for j in range(-1, 2):  #x
                if i == 0 and j == 0:
                    pass
                else:
                    if self.squareArray[(x+j)%self.squares][(y+i)%self.squares]:
                        count += 1
        return count

    def getCordsInArray(self, pos):
        x, y = pos
        x                 = int(x/(self.squareSize+1))
        y = int(y/(self.squareSize+1))
        return (x,y)

    def isAlive(self, x, y):
        count = self.aliveAround(x, y) 
        selfAlive = self.squareArray[x][y]
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

    def updateLife(self):
        new = [[False for x in range(self.squares)] for y in range(self.squares)]
        for i in range(self.squares):
            for j in range(self.squares):
                new[i][j]=self.isAlive(i,j)
        for i in range(self.squares):
            for j in range(self.squares):
                self.squareArray[i][j] = new[i][j]

    def drawSquares(self):
           for i in range(self.squares):
            for j in range (self.squares):
                if self.squareArray[i][j]:
                    self.fillSquare(i, j, self.white)
                else:
                    self.fillSquare(i, j, self.black)
    
    def drawSquare(self, x1, y1, x2, y2):
        startX = min(x1, x2)
        startY = min(y1, y2)
        red = 200, 0, 0
        for x in range(abs(x1-x2)+1):
            self.fillSquare(startX+x, y1, red)
            self.fillSquare(startX+x, y2, red)
        for y in range(abs(y1-y2) +1):
            self.fillSquare(x1, startY+y, red) 
            self.fillSquare(x2, startY+y, red)
        update()
        

    def openFileDialog(self): 
        root = tkinter.Tk()
        # root.withdraw()
        file = filedialog.askopenfile(initialdir = os.getcwd, 
	      					        title = "Select a File", 
	      							filetypes = (("Text files", 
	      										"*.txt*"), 
	      										("all files", 
	      										"*.*")))
        root.destroy()
        txt = file.read()
        return txt
    def saveFile(self, textToSave):
        try:
            root = tkinter.Tk()
            file = filedialog.asksaveasfile(initialdir = os.getcwd, 
    				    			title = "Save File", 
    				    			filetypes = (("Text files", 
    				    						"*.txt*"), 
    				    						("all files", 
    				    						"*.*")))
            root.destroy()
            file.write(textToSave)
        except:
            pass