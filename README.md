# GameAI #

## What is this repository for? ##

This project is used to manage all code developed for GameAI lecture at Uni Bonn.

Version: 0.1 (first project)

## Project 01 ##
Check out the [project description](https://docs.google.com/viewer?a=v&pid=sites&srcid=ZGVmYXVsdGRvbWFpbnxiaXRnYW1lYWl8Z3g6NTY1YjdkMTkzOWM4YjM1NA).

### Task 1 ###
* Understand `tic-tac-toe.py`
* Realize statistical 'strategy' for player X:
* Collect cell participation for wins
* Normalize count data
* Realize heuristical 'strategy' for player X:
* Evaluate move (Can I win? -> Can enemy win? -> Best probability)

### Task 2 ###
* Realize Connect4 similar to `tic-tac-toe.py`
* Realize GUI with user input
* Try to collect 'good move' statistics

## Project 02 ##
Check out the [Project description](https://docs.google.com/viewer?a=v&pid=sites&srcid=ZGVmYXVsdGRvbWFpbnxiaXRnYW1lYWl8Z3g6NmE4ZTEyNjNkZTQzNWVmYg).

### Task 1 ###
* Compute number of nodes in TicTacToe game tree
* Explain difference in numbers
* Compute complete game tree ignoring symmetries
* What is the number of nodes?
* How many nodes correspond to a win for X?
* What is the branching factor of the tree?

### Task 2 ###
* Implement MinMax algorithm
* Use the implementation to compute some MinMax results
* Consider tree with given MinMax value to its nodes
* Discuss a checking for alternatives in cases of ties

### Task 3 ###
* Implement MinMax search for Connect4
* Create an evaluation function
* Let the computer play a tournament and collect statistics
* **Bonus:** Update `connect_four.py` to implement any size of field

### Task 4 ###
* Implement controller for breakout
* Modify `breakout.py` to increase speed over time

### Task 5 ###
* Implement a program to read map data from a `.txt` file
* Put map data into a graph
* Implement Dijkstra's algorithm
* Implement A* algorithm and use Euclidean distance

## Project 03 ##

### TBD ###

## Presentation ##
The presentations are held using Jupyter Notebook. To start
the presentation just run:

`jupyter nbconvert Presentation.ipynb --to slides --post serve`

## How do I get set up? ##
To get the project on your system:

* You need to have Python 2.7.x or Python 3.x
* You need `git` to be installed on your system
* Run `git clone https://bitbucket.org/LeKono/game_ai.git` to clone the repo from BitBucket
* Run `git clone https://github.com/LeKono/gameAI.git` to clone the repo from GitHub

Get it started:

* Run `pip install -r requirements.txt` to install all python modules required to
run the code.

* `python tic_tac_toe_B.py` starts a game of TicTacToe on terminal
* `from tic_tac_toe_B import TicTacToe` is how you can import TicTacToe to a python environment.

* `python connect_four.py` starts a GUI
* `from connect_four import ConnectFour` can be used to import ConnectFour to a python environment.


### The Team ###

* Agarwal, Swasti
* Balci, Mehmet
* Biswas, Tonmoy
* Brüggemann, Thomas
* [Ibhaluobe, David](https://github.com/ibhal)
* Khan, Mohammad Asif Irfan
* Konotopez, Andrej
* Liu, Zhuofan
* Milchenski, Zdravko
* Rahman, Mahfuzur
