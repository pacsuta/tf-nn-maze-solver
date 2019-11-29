import numpy as np
import maze_collection as mc
import maze

MAX_STEPS = 20

m = maze.Maze(mc.T_maze)

cumulative = np.zeros_like(m.maze, np.int64)
cumulative[m.startY, m.startX] = 1

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

probabilities = np.zeros_like(cumulative, np.float64)
total_steps = np.sum(cumulative)
for y in range(len(cumulative)):
    for x in range(len(cumulative[y])):
        probabilities[y][x] = cumulative[y][x] / total_steps
print("All possible positions after 20 steps:")
print(cumulative)
print("\nTotal steps calculated:", total_steps)
print("\nProbabilities of all positions after 20 steps:")
print(probabilities)
print("\nSum of all probabilities:", np.sum(probabilities))
