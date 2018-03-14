#
#   CS6613 Artificial Intelligence
#   Project 1 Mini-Checkers Game
#   Shang-Hung Tsai
#


class AIPlayer():
    def __init__(self, game, difficulty):
        self.game = game
        self.difficulty = difficulty

    def getNextMove(self):
        if self.difficulty == 1:
            return self.getNextMoveEasy()

    def getNextMoveEasy(self):
        '''
        Simple AI, returns the first found legal move
        '''
        directions = [[1, -1], [1, 1], [2, -2], [2, 2]]
        for checker in self.game.opponentCheckers:
            position = self.game.checkerPositions[checker]
            print("Current checker: " + str(position))
            row = position[0]
            col = position[1]
            for dir in directions:
                print(str(row + dir[0]) + " " + str(col + dir[1]))
                if self.game.isValidMove(row, col, row + dir[0], col + dir[1], False):
                    print("----------------")

                    return row, col, row + dir[0], col + dir[1]
