# tf-nn-maze-solver
MSc project code, using TensorFlow to implement a neural network that can solve a small 2D maze with reinforcement learning

The "network....py" files are mostly the same. Run the file corresponding to the desired maze structure, or modify the code to suit another structure.

maze.py can be run on its own as an interactive maze. It can be controller with w, a, s, d inputs on the command line. The orange square is the player, the green square is the goal, black squares are walls, white squares are free spaces.

random_exploration.py calculates the chances of the agent being in any position after MAX_STEPS steps, provided the input is random. This does not take into account the victory condition of reaching the goal.

random_exploration2.py calculates the chances of the agent finding the goal in MAX_STEPS steps, provided the input is random.
