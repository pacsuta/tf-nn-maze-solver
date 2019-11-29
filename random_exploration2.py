import numpy as np
import maze_collection as mc
import maze

MAX_STEPS = 20

m = maze.Maze(mc.T_maze)

cumulative = np.zeros_like(m.maze, np.int64)
cumulative[m.startY, m.startX] = 1

victory_steps = np.zeros(MAX_STEPS)

for i in range(MAX_STEPS):
    change = np.zeros_like(cumulative)
    for y in range(len(m.maze)):
        for x in range(len(m.maze[y])):
            value = cumulative[y][x]
            if m.maze[y][x] != 1 and value > 0:
                m.x = x
                m.y = y
                if m.distance_up() > 0:
                    change[y-1][x] += value
                else:
                    change[y][x] += value
                if m.distance_down() > 0:
                    change[y+1][x] += value
                else:
                    change[y][x] += value
                if m.distance_left() > 0:
                    change[y][x-1] += value
                else:
                    change[y][x] += value
                if m.distance_right() > 0:
                    change[y][x+1] += value
                else:
                    change[y][x] += value
            change[y][x] -= value
    cumulative += change
    victory_steps[i] = cumulative[0][0]
    cumulative[0][0] = 0

for v_pos, v in enumerate(victory_steps):
    all_permutations = pow(4, v_pos+1)
    for i in range(v_pos):
        # The agents that have reached the goal are no longer taking steps and creating permutations!
        all_permutations -= victory_steps[i]
    print("Victories in {0} steps: {1} (Probability at this point: P({0}) = {2})".format(v_pos+1, v,
                                                                                         v/all_permutations))
