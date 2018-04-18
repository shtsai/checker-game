# Mini-Checkers Game
## Description
This game is a modified version of the traditional 8 x 8 checkers game. The rules are similar to the original game, except a few differences. Below is a summary of the game rules.
1. The game is played on a 6 x 6 checkers board.
2. Each player starts out with six pieces.
3. At the start of the game, the human player can choose to move first or second.
4. Each player takes turn to make a move.
5. There are two types of moves: regular move and capture move. 
    * In a regular move,a checker can move forward diagonally to an adjacent square that is empty.
    * In a capture move,a piece can jump over and capture an opponent’s piece and land on an empty square (landing on a square that is not empty is not allowed.) The jump must be in the forward diagonal direction and no consecutive jumps are allowed. In addition, every opportunity to jump must be taken. In the case where there are two or more possible jump moves, the player can choose which one to take.
6. No vertical,horizontal or backward moves are allowed for both regular and capture moves.
7. If a player has no legal move to take, his/her turn will be forfeited and the other player will make the next move.
8. A player wins when he/she captures all of the other player’s pieces. If both players do not have any legal move to take, the game will end and the player with the most number of pieces left wins; if the two players have the same number of pieces left, the game is a draw.


## Compilation and Run
This Mini-Checkers game is written in Python 3. 

For the graphical user interface, it uses the Tkinter library, which is a built-in library that comes with Python 3. So you should not need to install additional packages to run the program.

To run the game, type the following command in the terminal:
```
python3 main.py 
```

In the command line, you will first see:
```
Do you want to go first? (Y/N)
```
Enter Y if you want to go first. Otherwise, enter N. 

Next, you will see the second question:
```
What level of difficulty? (1 Easy, 2 Medium, 3 Hard)
```
Enter the level of difficulty you want, either 1, 2, or 3.

You will see a checker board pops up in a new window. You can make moves by first clicking on the checker and then clicking on the destination block on the board.


## Design and Architecture
The program consists of four parts:
*	main.py: This is the entry point of the program. You run this file to start the game.
*	CheckerGame.py: This file manages all the logics of the mini-checkers game. It maintains the states of the game and checker board. It checks if a move is legal and applies the move to the board. It also keeps track of whose turn it is and whether the game has ended.
*	AIPlayer.py: The file contains the logic for AI player. The AI player uses Alpha-Beta Search to determine the best move to make.
*	BoardGUI.py: The is the graphical user interface of the game. It brings up a checker board with checkers on it. Players can make moves by clicking on the checkers and move them around. 


## Implementation Details
### Terminal state: 
There are three possible terminal states.
1. Human player has zero checkers left.
2. AI player has zero checkers left.
3. Human player and AI player both have no moves left.

### Utility function: 
Once the game reaches a terminal state, we compute the utility value. 
The utility value is defined as following:

> Utility value = (number of AI checkers – number of human checkers) * 500 
                         + number of AI checkers * 50
                         
The most important goal of the game is to have more checkers left than your component, therefore I assign a weight of 500 to the difference in the number of checkers. In addition, if the difference in the number of checkers is the same, the AI player would like to have as many checkers left as possible. So a weight of 50 is assigned to the number of remaining AI checkers.

Note that the weights in the utility function are pretty high, because this allows the AI player to prefer a utility value (produced from a deterministic terminal state) over a heuristics value (which is just an estimate).

### Search cut-off and depth limit:
Since we have a time limit of 15 seconds for each move, sometimes it is impossible to do a complete search of the game state. Therefore, I integrate a cut-off feature in the Alpha Beta Search. Before each search, I specify a depth limit. If the search algorithm reaches the depth limit, it will terminate the search and compute a heuristic value using the evaluation function based on the game state it found. This guarantees that the AI player will come up with a move within the time limit.

The depth limit is dynamically computed, and it is negatively correlated with the total number of checkers left. The more checkers we have, the more branches the search tree will generate. Therefore, the AI player starts with a lower depth limit. As the total number of checkers decreases, the search depth limit gradually increases.

### Evaluation function (heuristics): 
If the search reaches the depth limit, the AI player calls the evaluation function to get a heuristics value of the current path. The evaluation function is defined as following:

> Heuristic value = (number of AI checkers – number of human checkers) * 50
                            + number of safe AI checkers * 10 
                            + number of AI checkers

Same as before, the difference in number of checkers between two players is important, so it is assigned a weight of 50. In addition, we count the number of safe AI checkers and multiply that by 10. A safe AI checker is a checker that the opponent cannot capture. It is defined as a checker that either is on the boundary of the board (leftmost and rightmost columns) or has passed all of the opponent checkers. Lastly, the heuristic value also takes into account of the number of AI checkers left.

Note that weights in the evaluation function are lower than the weights in the utility function. This makes sure that heuristics values are always smaller than utility values and utility values are preferred by the AI player, because utility values lead to deterministic results.

### Levels of difficulty
Three levels of difficulty are implemented in this game.
1. Easy: The AI player simply makes a random choice among all the available legal moves.
2. Medium: The AI player uses Alpha Beta search with a uniform search depth limit of 5.
3. Hard: The AI player uses Alpha Beta search with a dynamic search depth limit. The search depth is around 14 – 20. 
