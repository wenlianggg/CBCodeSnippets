# Wen Liang Goh - https://github.com/wenlianggg
# 29 April 2020
# Snake game within a 7x7 grid, with an initial length of 4


class Snake():
    def __init__(self, length: int, row: int, col: int):
        self.queue = []
        for i in range(length):
            self.queue.append([row, col])  # [4,3] [5,3] [6,3] [6,4]

    def move(self, direction: str, grow: bool):
        headx, heady = self.queue[-1]
        if direction == 'N':
            self.queue.append([headx - 1, heady])
        elif direction == 'S':
            self.queue.append([headx + 1, heady])
        elif direction == 'E':
            self.queue.append([headx, heady + 1])
        elif direction == 'W':
            self.queue.append([headx, heady - 1])
        if not grow:
            self.queue.pop(0)

    def get_state(self, grid: list):
        for x, y in self.queue:
            grid[x][y] = 1
        return grid


def grid_generator(w, h):
    return [[0 for x in range(w)] for y in range(h)]


def grid_printer(grid):
    for row in grid:
        print(*row, sep=" ")


if __name__ == "__main__":
    w, h = 7, 7
    snake = Snake(4, 1, 3)
    grid_printer(snake.get_state(grid_generator(w, h)))
    while True:
        direction = str(input("Enter direction (N/S/E/W): "))
        growth = bool(input("Enter something if it has eaten: "))
        snake.move(direction, growth)
        grid_printer(snake.get_state(grid_generator(w, h)))
