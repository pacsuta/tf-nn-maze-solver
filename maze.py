import graphics as g
import maze_collection as mc


class Maze:
    def __init__(self, maze_type):
        # Use the maze types from maze_collection.py
        [self.maze,
         [self.startX, self.startY],
         [self.goalX, self.goalY]] = maze_type
        self.x = self.startX
        self.y = self.startY

        self.won = False

        self.win = None
        self.squares = None

    def reset(self):
        self.x = self.startX
        self.y = self.startY

        self.won = False
        if self.win is not None:
            self.display()

    def display_commandline(self):
        to_print = ""
        for y_pos, y in enumerate(self.maze):
            for x_pos, x in enumerate(y):
                if self.x == x_pos and self.y == y_pos:
                    to_print += " O "
                elif self.goalX == x_pos and self.goalY == y_pos:
                    to_print += " X "
                elif x == 0:
                    to_print += "   "
                elif x == 1:
                    to_print += " # "
            to_print += "\n"
        print(to_print)

    def initialise_graphics(self):
        self.win = g.GraphWin("Maze", 200 + (50 * len(self.maze[0])), 200 + (50 * len(self.maze)))
        self.squares = []
        for i in range(len(self.maze)):
            self.squares.append([])
            for j in range(len(self.maze[i])):
                self.squares[i].append(
                    g.Rectangle(g.Point(100 + (j * 50), 100 + (i * 50)), g.Point(150 + (j * 50), 150 + (i * 50))))
                self.squares[i][j].draw(self.win)
        self.display()

    def display(self):
        for y_pos, y in enumerate(self.maze):
            for x_pos, x in enumerate(y):
                if self.x == x_pos and self.y == y_pos:
                    self.squares[y_pos][x_pos].setFill("orangered")
                elif self.goalX == x_pos and self.goalY == y_pos:
                    self.squares[y_pos][x_pos].setFill("green")
                elif x == 0:
                    self.squares[y_pos][x_pos].setFill("white")
                elif x == 1:
                    self.squares[y_pos][x_pos].setFill("black")

    def check_win_condition(self):
        if self.x == self.goalX and self.y == self.goalY:
            self.won = True

    def move_up(self):
        if self.y - 1 >= 0 and self.maze[self.y - 1][self.x] != 1:
            self.y -= 1
        self.check_win_condition()

    def move_down(self):
        if self.y + 1 < len(self.maze) and self.maze[self.y + 1][self.x] != 1:
            self.y += 1
        self.check_win_condition()

    def move_left(self):
        if self.x - 1 >= 0 and self.maze[self.y][self.x - 1] != 1:
            self.x -= 1
        self.check_win_condition()

    def move_right(self):
        if self.x + 1 < len(self.maze[0]) and self.maze[self.y][self.x + 1] != 1:
            self.x += 1
        self.check_win_condition()

    def distance_up(self):
        for i in range(self.y, -1, -1):
            if i - 1 < 0 or self.maze[i - 1][self.x] == 1:
                return self.y - i

    def distance_down(self):
        for i in range(self.y, len(self.maze), 1):
            if i + 1 >= len(self.maze) or self.maze[i + 1][self.x] == 1:
                return i - self.y

    def distance_left(self):
        for i in range(self.x, -1, -1):
            if i - 1 < 0 or self.maze[self.y][i - 1] == 1:
                return self.x - i

    def distance_right(self):
        for i in range(self.x, len(self.maze[0]), 1):
            if i + 1 >= len(self.maze) or self.maze[self.y][i + 1] == 1:
                return i - self.x

    def normal_x(self):
        return self.x / (len(self.maze[0]) - 1)

    def normal_y(self):
        return self.y / (len(self.maze) - 1)

    def normal_goal_x(self):
        return self.goalX / (len(self.maze[0]) - 1)

    def normal_goal_y(self):
        return self.goalY / (len(self.maze) - 1)


def play_commandline():
    maze = Maze(mc.T_maze)
    while not maze.won:
        maze.display_commandline()
        print("Up:", maze.distance_up())
        print("Down:", maze.distance_down())
        print("Left:", maze.distance_left())
        print("Right:", maze.distance_right())
        x = input()
        if x[0] == "w":
            maze.move_up()
        elif x[0] == "s":
            maze.move_down()
        elif x[0] == "a":
            maze.move_left()
        elif x[0] == "d":
            maze.move_right()
    print("Congratulations! You won!")


def play_graphics():
    maze = Maze(mc.U_maze)
    maze.initialise_graphics()
    while not maze.won:
        x = input()
        if x[0] == "w":
            maze.move_up()
            maze.display()
        elif x[0] == "s":
            maze.move_down()
            maze.display()
        elif x[0] == "a":
            maze.move_left()
            maze.display()
        elif x[0] == "d":
            maze.move_right()
            maze.display()
    print("Congratulations! You won!")


def main():
    # play_commandline()
    play_graphics()


if __name__ == "__main__":
    main()
