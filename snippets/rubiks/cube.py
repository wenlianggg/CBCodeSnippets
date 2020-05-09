# Wen Liang Goh - https://github.com/wenlianggg
# 8-9 May 2020
# Rubiks Cube Mover and Visualisation
# Utility to recreate Rubiks' cube movements (but not solving them)
# Coloured plot view requires Matplotlib and Numpy installed.

from collections import defaultdict
try:  # Try and import optional dependencies
    import matplotlib.pyplot as plt
    from matplotlib import colors
    import numpy as np
except ImportError:
    plt = None
    colors = None
    np = None


class Cube():
    def __init__(self):

        self.cube = defaultdict(list)
        for colour in ['O', 'G', 'R', 'B', 'W', 'Y']:
            self.cube[colour] = [[f'{colour}', f'{colour}', f'{colour}'] for x in range(3)]

    def __getitem__(self, key):
        return self.cube[key]

    def __setitem__(self, key, value):
        self.cube[key] = value

    def rotate_face(self, cube_side: str):
        self.cube[cube_side] = [list(cubeside) for cubeside in zip(*reversed(self.cube[cube_side]))]

    def get_col(self, cube_side: str, colidx: int):
        return [row[colidx] for row in self.cube[cube_side]]

    def get_row(self, cube_side: str, rowidx: int):
        return self.cube[cube_side][rowidx][:]

    def set_col(self, cube_side: str, colidx: int, newvals: list, reverse=False):
        if reverse:
            newvals = list(reversed(newvals))
        for row in range(3):
            self.cube[cube_side][row][colidx] = newvals[row]

    def set_row(self, cube_side: str, rowidx: int, newvals: list, reverse=False):
        if reverse:
            newvals = list(reversed(newvals))
        for col in range(3):
            self.cube[cube_side][rowidx][col] = newvals[col]

    def getplotdata(self):
        def to_ccode(colour):
            switcher = {
                'O': 10,
                'G': 20,
                'R': 30,
                'B': 40,
                'W': 50,
                'Y': 60
            }
            return switcher.get(colour, "Invalid Colour")

        data = []

        for i in range(3):
            data.append([0, ] * 3 + [to_ccode(x) for x in self.cube['W'][i]] + [0, ] * 6)
        for i in range(3):
            sublist = []
            sublist.extend([to_ccode(x) for x in self.cube['O'][i]])
            sublist.extend([to_ccode(x) for x in self.cube['G'][i]])
            sublist.extend([to_ccode(x) for x in self.cube['R'][i]])
            sublist.extend([to_ccode(x) for x in self.cube['B'][i]])
            data.append(sublist)
        for i in range(3):
            data.append([0, ] * 3 + [to_ccode(x) for x in self.cube['Y'][i]] + [0, ] * 6)

        return np.asarray(data)

    def plot(self, nparray):
        plt.close()
        cmap = colors.ListedColormap(['black', 'orange', 'lightgreen', 'red', 'blue', 'white', 'yellow'])
        bounds = [0, 10, 20, 30, 40, 50, 60, 70]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        fig, ax = plt.subplots()
        fig.canvas.set_window_title('Rubiks Cube')
        ax.imshow(nparray, cmap=cmap, norm=norm)
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

        # draw gridlines
        ax.grid(which='major', linestyle='-', color='k', linewidth=2)
        ax.set_xticks(np.arange(0.5, 12.5, 1))
        ax.set_yticks(np.arange(0.5, 9.5, 1))
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        plt.show(block=False)
