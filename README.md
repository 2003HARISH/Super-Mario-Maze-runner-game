
# Super Mario Maze runner game

This is a simple game called Super Mario Maze Runner implemented using the Pygame library. The game generates a random maze using a randomized depth-first search algorithm called the "Recursive Backtracker" algorithm. The player controls a character and navigates through the maze to reach the exit

## Game Mechanics
The player can control the character using the arrow keys on the keyboard. The objective is to reach the exit of the maze to complete each level. The maze is randomly generated for each level, and the difficulty increases with each level.

The player character cannot move through walls, so the player needs to find the correct path to reach the exit without colliding with the walls. Collision detection is implemented to detect when the player collides with the walls or the exit block.

## Installation and Usage
1. Clone the repository to your local machine.
2. Make sure you have Python and Pygame installed.
3. Run the maze_runner.py file using Python.
4. Use the arrow keys to control the player character.
5. Navigate through the maze and reach the exit to complete  each level.
6. Enjoy playing Maze Runner!


## Algorithm

The algorithm being used in this code is a randomized depth-first search algorithm to generate a maze. Specifically, it is using the "Recursive Backtracker" algorithm, where the algorithm starts at a random cell, chooses a random direction to move, and then recursively explores each cell it encounters until it reaches a dead-end. When it reaches a dead-end, the algorithm backtracks until it finds a cell with unexplored neighbors and continues. The algorithm is implemented in the generate_maze() function.