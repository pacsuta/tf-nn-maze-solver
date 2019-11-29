
# Structure:
# X_maze = [layout, start_coordinates, goal_coordinates]

# Layout:
# 0 = Free space
# 1 = Wall

T_maze = [
    [  # Layout
        [0, 0, 0],
        [1, 0, 1],
        [1, 0, 1]
    ],
    [1, 2],  # Start coordinates
    [0, 0]   # Goal coordinates
]

U_maze = [
    [  # Layout
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0]
    ],
    [0, 0],  # Start coordinates
    [2, 0]   # Goal coordinates
]

line_maze = [
    [  # Layout
        [1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0]
    ],
    [0, 1],  # Start coordinates
    [6, 1]   # Goal coordinates
]

H_maze = [
    [  # Layout
        [0, 1, 0],
        [0, 0, 0],
        [0, 1, 0]
    ],
    [0, 2],  # Start coordinates
    [2, 0]   # Goal coordinates
]

simple_maze = [
    [  # Layout
        [1, 1],
        [0, 0]
    ],
    [0, 1],  # Start coordinates
    [1, 1]   # Goal coordinates
]

simple_maze1 = [
    [  # Layout
        [1, 1, 1],
        [1, 0, 0]
    ],
    [1, 1],  # Start coordinates
    [2, 1]   # Goal coordinates
]

default_maze = [
    [  # Layout
        [0],
        [0]
    ],
    [0, 1],  # Start coordinates
    [0, 0]   # Goal coordinates
]