# Flappy Bird Using Neuroevolution 

## Introduction

Toy problems, like games, have a long history of being used in the development of artificial intelligence. This is exemplified through revolutionary projects like Deep Blue and Open AI Gym. In this project, this concept is extended to the game Flappy Bird. The game is developed and the agent is trained to play the game by itself using a neuroevolution algorithm. The analysis includes the comparison of various crossovers and fitness functions. The development of the AI algorithms are done primarily from scratch, just using NumPy. Through the combination of a complex fitness function and variable-point crossover an unbeatable agent was developed.

## Running the Code

In order to have the client play the game, ensure the following packages are installed with Python 3:

- pygame
- numpy

Ensure that the following files and folders are kept in the same directory:

- /Sounds/
- /Images/ 
- Bird.py
- Game.py
- GeneticAlgorithm.py
- NeuralNetwork.py
- Pipe.py

The agent and training can be launched from the command-line by navigating to the directory and executing through the following:

~~~
python Game.py
~~~

In order to change the fitness function, crossover function, or activation modify the following excerpt of code present in Game.py:

~~~
# Learning functions
fitness_type = "complex"
crossover_type = "variable"
activation_type = "tanh"
~~~

The options for the above are given as follows:

| Function Type   | Options                     |
|-----------------|-----------------------------|
| fitness_type    | "simple", "complex"         |
| crossover_type  | "none", "fixed", "variable" |
| activation_type | "tanh", "relu"              |
