#
#   CS6613 Artificial Intelligence
#   Project 1 Mini-Checkers Game
#   Shang-Hung Tsai
#

import tkinter
from CheckerGame import *

class BoardGUI():
    def __init__(self, game):
        # Initialize parameters
        self.game = game
        self.ROWS = 6
        self.COLS = 6
        self.WINDOW_WIDTH = 600
        self.WINDOW_HEIGHT = 600
        self.col_width = self.WINDOW_WIDTH / self.COLS
        self.row_height = self.WINDOW_HEIGHT / self.ROWS

        # Initialize GUI
        self.initBoard()

    def initBoard(self):
        self.root = tkinter.Tk()
        self.c = tkinter.Canvas(self.root, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT,
                                borderwidth=5, background='white')
        self.c.pack()
        self.board = [[0]*self.COLS for _ in range(self.ROWS)]
        self.tiles = [[None for _ in range(self.COLS)] for _ in range(self.ROWS)]

        # Print dark square
        for i in range(6):
            for j in range(6):
                if (i + j) % 2 == 1:
                    self.c.create_rectangle(i * self.row_height, j * self.col_width,
                                        (i+1) * self.row_height, (j+1) * self.col_width, fill="gray", outline="gray")

        # Print grid lines
        for i in range(6):
            self.c.create_line(0, self.row_height * i, self.WINDOW_WIDTH, self.row_height * i, width=2)
            self.c.create_line(self.col_width * i, 0, self.col_width * i, self.WINDOW_HEIGHT, width=2)

        # Place checks on the board
        self.updateBoard()

        # Initialize parameters
        self.checkerSelected = False
        self.clickData = {"row": 0, "col": 0, "checker": None}

        # Register callback function for mouse clicks
        self.c.bind("<Button-1>", self.processClick)

        # make GUI updates board every second
        self.root.after(1000, self.updateBoard)


    def startGUI(self):
        self.root.mainloop()

    def pauseGUI(self):
        self.c.bind("<Button-1>", '')

    def resumeGUI(self):
        self.c.bind("<Button-1>", self.processClick)

    # Update the positions of checkers
    def updateBoard(self):
        if self.game.isBoardUpdated():
            newBoard = self.game.getBoard()
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] != newBoard[i][j]:
                        self.board[i][j] = newBoard[i][j]
                        self.c.delete(self.tiles[i][j])
                        self.tiles[i][j] = None

                        # choose different color for different player's checkers
                        if newBoard[i][j] < 0:
                            self.tiles[i][j] = self.c.create_oval(j*self.col_width+10, i*self.row_height+10,
                                                              (j+1)*self.col_width-10, (i+1)*self.row_height-10,
                                                              fill="black")
                        elif newBoard[i][j] > 0:
                            self.tiles[i][j] = self.c.create_oval(j*self.col_width+10, i*self.row_height+10,
                                                                  (j+1)*self.col_width-10, (i+1)*self.row_height-10,
                                                                  fill="red")
                        else:  # no checker
                            continue

                        # raise the tiles to highest layer
                        self.c.tag_raise(self.tiles[i][j])

            # tell game logic that GUI has updated the board
            self.game.completeBoardUpdate()

        # make GUI updates board every second
        self.root.after(1000, self.updateBoard)

    # this function checks if the checker belongs to the current player
    # if isPlayerTurn() returns True, then it is player's turn and only
    # postive checkers can be moved. Vice versa.
    def isCurrentPlayerChecker(self, row, col):
        return self.game.isPlayerTurn() == (self.board[row][col] > 0)

    # callback function that process user's mouse clicks
    def processClick(self, event):
        col = int(event.x // self.col_width)
        row = int(event.y // self.row_height)

        # If there is no checker being selected
        if not self.checkerSelected:
            # there exists a checker at the clicked position
            # and the checker belongs to the current player
            if self.board[row][col] != 0 and self.isCurrentPlayerChecker(row, col):
                self.clickData["row"] = row
                self.clickData["col"] = col
                self.clickData["color"] = self.c.itemcget(self.tiles[row][col], 'fill')

                # replace clicked checker with a temporary checker
                self.c.delete(self.tiles[row][col])
                self.tiles[row][col] = self.c.create_oval(col*self.col_width+10, row*self.row_height+10,
                                                         (col+1)*self.col_width-10, (row+1)*self.row_height-10,
                                                          fill="green")
                self.checkerSelected = True

            else: # no checker at the clicked postion
                return

        else: # There is a checker being selected
            # First reset the board
            oldrow = self.clickData["row"]
            oldcol = self.clickData["col"]
            self.c.delete(self.tiles[oldrow][oldcol])
            self.tiles[oldrow][oldcol] = self.c.create_oval(oldcol*self.col_width+10, oldrow*self.row_height+10,
                                                            (oldcol+1)*self.col_width-10, (oldrow+1)*self.row_height-10,
                                                            fill=self.clickData["color"])

            # If the destination leads to a legal move
            self.game.move(self.clickData["row"], self.clickData["col"],row, col)
            self.checkerSelected = False


