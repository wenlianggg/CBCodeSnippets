# Wen Liang Goh - https://github.com/wenlianggg
# 8-9 May 2020
# Rubiks Cube Mover and Visualisation
# Utility to recreate Rubiks' cube movements (but not solving them)
# Coloured plot view requires Matplotlib and Numpy installed.

from collections import defaultdict

def display(cube: dict):
    for rowid in range(3):
        print(' '*5, " ".join(cube['W'][rowid]), sep="|", end="|\n")
    for rowid in range(3):
        print(" ".join(cube['O'][rowid]), " ".join(cube['G'][rowid]), " ".join(cube['R'][rowid]), " ".join(cube['B'][rowid]), sep="|")
    for rowid in range(3):
        print(' '*5, " ".join(cube['Y'][rowid]), sep="|", end="|\n")
    print()

def set_col(cube_side: list, colidx: int, newvals: list, reverse=False):
    if reverse:
        newvals = list(reversed(newvals))
    for row in range(3):
        cube_side[row][colidx] = newvals[row]

def set_row(cube_side: list, rowidx: int, newvals: list, reverse=False):
    if reverse:
        newvals = list(reversed(newvals))
    for col in range(3):
        cube_side[rowidx][col] = newvals[col]

def move(cube: dict, direction: str):
    if direction == "F":
        cube['G'] = [list(cubeside) for cubeside in zip(*reversed(cube['G']))]

        tmp_u = cube['W'][2][:]
        tmp_r = [row[0] for row in cube['R']]
        tmp_d = cube['Y'][0][:]
        tmp_l = [row[2] for row in cube['O']]

        set_col(cube['R'], 0, tmp_u)
        set_row(cube['Y'], 0, tmp_r, reverse=True)
        set_col(cube['O'], 2, tmp_d)
        set_row(cube['W'], 2, tmp_l, reverse=True)

    if direction == "R":
        cube['R'] = [list(cubeside) for cubeside in zip(*reversed(cube['R']))]

        tmp_u = [row[2] for row in cube['W']]
        tmp_r = [row[0] for row in cube['B']]
        tmp_d = [row[2] for row in cube['Y']]
        tmp_l = [row[2] for row in cube['G']]

        set_col(cube['B'], 0, tmp_u, reverse=True)
        set_col(cube['Y'], 2, tmp_r, reverse=True)
        set_col(cube['G'], 2, tmp_d)
        set_col(cube['W'], 2, tmp_l)

    if direction == "U":
        cube['W'] = [list(cubeside) for cubeside in zip(*reversed(cube['W']))]

        tmp_u = cube['O'][0][:]
        tmp_r = cube['B'][0][:]
        tmp_d = cube['R'][0][:]
        tmp_l = cube['G'][0][:]

        set_row(cube['B'], 0, tmp_u)
        set_row(cube['R'], 0, tmp_r)
        set_row(cube['G'], 0, tmp_d)
        set_row(cube['O'], 0, tmp_l)


    if direction == "B":
        cube['B'] = [list(cubeside) for cubeside in zip(*reversed(cube['B']))]

        tmp_u = cube['W'][0][:]
        tmp_r = [row[0] for row in cube['O']]
        tmp_d = cube['Y'][2][:]
        tmp_l = [row[2] for row in cube['R']]

        set_col(cube['O'], 0, tmp_u, reverse=True)
        set_row(cube['Y'], 2, tmp_r)
        set_col(cube['R'], 2, tmp_d, reverse=True)
        set_row(cube['W'], 0, tmp_l)

    if direction == "L":
        cube['O'] = [list(cubeside) for cubeside in zip(*reversed(cube['O']))]

        tmp_u = [row[0] for row in cube['W']]
        tmp_r = [row[0] for row in cube['G']]
        tmp_d = [row[0] for row in cube['Y']]
        tmp_l = [row[2] for row in cube['B']]

        set_col(cube['G'], 0, tmp_u)
        set_col(cube['Y'], 0, tmp_r)
        set_col(cube['B'], 2, tmp_d, reverse=True)
        set_col(cube['W'], 0, tmp_l, reverse=True)

    if direction == "D":
        cube['Y'] = [list(cubeside) for cubeside in zip(*reversed(cube['Y']))]

        tmp_u = cube['G'][2][:]
        tmp_r = cube['R'][2][:]
        tmp_d = cube['B'][2][:]
        tmp_l = cube['O'][2][:]

        set_row(cube['R'], 2, tmp_u)
        set_row(cube['B'], 2, tmp_r)
        set_row(cube['O'], 2, tmp_d)
        set_row(cube['G'], 2, tmp_l)

    return cube

cube = defaultdict(list)

for colour in ['O', 'G', 'R', 'B', 'W', 'Y']:
    cube[colour] = [[f'{colour}',f'{colour}',f'{colour}'] for x in range(3)]

userinput = input("Enter moves (F/R/U/B/L/D), separated by spaces: ").upper()
moves = userinput.split()

for direction in moves:
    move(cube, direction)

display(cube)

try:
    import matplotlib.pyplot as plt
    from matplotlib import colors
    import numpy as np
except ImportError:
    external_module = None

if np and plt:
    def to_ccode(colour):
        if colour == "O": return 10
        if colour == "G": return 20
        if colour == "R": return 30
        if colour == "B": return 40
        if colour == "W": return 50
        if colour == "Y": return 60

    data = []

    for i in range(3):
        data.append([0,]*3+[to_ccode(x) for x in cube['W'][i]]+[0,]*6)
    for i in range(3):
        data.append([to_ccode(x) for x in cube['O'][i]]
                + [to_ccode(x) for x in cube['G'][i]]
                + [to_ccode(x) for x in cube['R'][i]]
                + [to_ccode(x) for x in cube['B'][i]])
    for i in range(3):
        data.append([0,]*3+[to_ccode(x) for x in cube['Y'][i]]+[0,]*6)

    npdata = np.asarray(data)
    cmap = colors.ListedColormap(['black', 'orange', 'lightgreen', 'red', 'blue', 'white', 'yellow'])
    bounds = [0,10,20,30,40,50,60,70]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    fig, ax = plt.subplots()
    fig.canvas.set_window_title('Rubiks Cube')
    ax.imshow(data, cmap=cmap, norm=norm)
    print(npdata)

    # draw gridlines
    ax.grid(which='major', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(0.5, 12.5, 1))
    ax.set_yticks(np.arange(0.5, 9.5, 1))
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    plt.show()
    
else:
    print("You do not have matplotlib and numpy installed, and thus you dont get to view generated pictures :(.")
