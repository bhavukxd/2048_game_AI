**2048 Game Solving and Analysis**
This repository contains the implementation of AI algorithms designed to solve the 2048 game effectively. The project explores advanced computational techniques to maximize scores and reach higher-value tiles, demonstrating applications of artificial intelligence in dynamic decision-making.

**Project Overview**
The 2048 game is a combinatorial puzzle where players merge numbered tiles on a 4x4 grid to achieve the target tile value of 2048 or beyond. While simple in concept, the game demands strategic planning and adaptability to avoid deadlocks and maximize long-term outcomes. This project implements and analyzes various AI techniques to automate and optimize gameplay.

**Key Features**
**Heuristic-Based Evaluation:** Simple, computationally efficient strategies using predefined rules like prioritizing empty tiles, cornering high-value tiles, and maximizing merges.
**Priority-Based Scoring**: Adds weighted scoring metrics, considering alignment, grid complexity, and corner strategy for improved decision-making.
**Mo****nte Carlo Tree Search** (**MCTS**): A probabilistic algorithm simulating future states to evaluate moves based on their long-term potential.
**Explicit Min-Max Algorithm**: A deterministic approach balancing player moves and random tile placement probabilities for optimal gameplay.


**CODE**
ai1.py-heuristic
aim.py-montecarlo
aip.py-priority
aimax.py-explicit Min-max
logic.py-logic ,movements of game
constant.py-colors,according to number 
puzzle.py-gui of game
json files-to store scores 
