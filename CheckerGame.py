#
#   CS6613 Artificial Intelligence
#   Project 1 Mini-Checkers Game
#   Shang-Hung Tsai
#

import tkinter
from BoardGUI import *

class CheckerGame():
    def __init__(self):
        self.board = self.initBoard()
        self.playerTurn = True
       # self.whoGoFirst()
        self.GUI = BoardGUI(self)

    # Let player decides to go first or second
    def whoGoFirst(self):
        ans = input("Do you want to go first? (Y/N) ")
        if ans == "Y" or ans == "y":
            self.playerTurn = True
        else:
            self.playerTurn = False

    # This function initializes the game board.
    # Each checker has a label. Positive checkers for the player,
    # and negative checkers for the opponent.
    def initBoard(self):
        board = [[0]*6 for _ in range(6)]
        for i in range(6):
            if i % 2 == 0:
                board[1][i] = -(i + 1)
                board[5][i] = i + 1
            else:
                board[0][i] = -(i + 1)
                board[4][i] = i + 1
        return board

    def getBoard(self):
        return self.board

    def printBoard(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                check = self.board[i][j]
                if (check < 0):
                    print(check,end=' ')
                else:
                    print(' ' + str(check),end=' ')

            print()

    def isPlayerTurn(self):
        return self.playerTurn

    def changePlayerTurn(self):
        self.playerTurn = not self.playerTurn

    def move(self, oldrow, oldcol, row, col):
        if not self.isValidMove(oldrow, oldcol, row, col):
            return False

        self.board[row][col] = self.board[oldrow][oldcol]
        self.board[oldrow][oldcol] = 0
        self.changePlayerTurn()
        return True

    def isValidMove(self, oldrow, oldcol, row, col):
        # No checker exists in original position
        if self.board[oldrow][oldcol] == 0:
            return False
        # Another checker exists in destination position
        if self.board[row][col] != 0:
            return False

        # player's turn
        if self.playerTurn:
            if row - oldrow == -1:   # regular move
                return abs(col - oldcol) == 1
            elif row - oldrow == -2:  # capture move
                if col - oldcol == -2 and self.board[row+1][col+1] < 0:  # \ direction
                    return True
                elif col - oldcol == 2 and self.board[row+1][col-1] < 0:  # / direction
                    return True
                else:
                    return False
            else:
                return False
        # opponent's turn
        else:
            if row - oldrow == 1:
                return abs(col - oldcol) == 1
            elif row - oldrow == 2:
                if col - oldcol == -2 and self.board[row-1][col+1] > 0: # / direction
                    return True
                elif col - oldcol == 2 and self.board[row-1][col-1] > 0: # \ direction
                    return True
                else:
                    return False
            else:
                return False

