Solitaire made for COMPSCI130 (with a personal twist!)

Overview:
This project is a simple python programme of a solitaire card game. 
The goal is to arrange the all the cards in descending order. The less moves, the higher the score.

Key Features:
Game Mechanics:
Move cards between piles, ensuring they are placed in descending order.
Discard pile which moves the top card to the bottom of the stack.
Undo implementation.
Hints that suggest the next best possible move

Scoring and High Score:
Score is calculated based on moves and hints used.
High score is recorded and shown at the end of each game.

Usage:
Start: Create a deck of cards as a python list ensuring all nujmbers are consecutive to each other. eg [3, 2, 1]. 
Commands: Press m to move, u to undo, or h for a hint.
Ending: The game will end when cards are correctly arranged or there are no possible moves.
