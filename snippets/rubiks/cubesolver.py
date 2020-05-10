# Wen Liang Goh - https://github.com/wenlianggg
# 8-9 May 2020
# Rubiks Cube Mover and Visualisation
# Utility to recreate Rubiks' cube movements (but not solving them)
# Coloured plot view requires Matplotlib and Numpy installed.

from cube import Cube
try:  # Try and import optional dependencies
    import matplotlib.pyplot as plt
    from matplotlib import colors
    import numpy as np
except ImportError:
    plt = None
    colors = None
    np = None


def main():
    cube = Cube()
    userinput = ""
    while True:
        userinput = input("Enter moves separated by spaces (F/R/U/B/L/D), or anything else to exit: ").upper()
        moves = userinput.split()
        for direction in moves:
            if direction not in ['F', 'R', 'U', 'B', 'L', 'D']:
                print(f"Exiting... Input '{direction}' unrecognised!")
                return
            move(cube, direction)
        if np and plt and colors:  # Dependencies are present
            nparray = cube.getplotdata()
            cube.plot(nparray)
        else:
            display(cube)


def display(cube: dict):
    for rowid in range(3):
        print(' ' * 5, " ".join(cube['W'][rowid]), sep="|", end="|\n")
    for rowid in range(3):
        print(" ".join(cube['O'][rowid]), " ".join(cube['G'][rowid]), " ".join(cube['R'][rowid]), " ".join(cube['B'][rowid]), sep="|")
    for rowid in range(3):
        print(' ' * 5, " ".join(cube['Y'][rowid]), sep="|", end="|\n")
    print()


def move(cube: Cube, direction: str):

    # Direction F(Green), B(Blue) - R C R C
    if direction == "F":
        cube.rotate_face('G')
        tmp_u = cube.get_row('W', 2)
        tmp_r = cube.get_col('R', 0)
        tmp_d = cube.get_row('Y', 0)
        tmp_l = cube.get_col('O', 2)
        cube.set_col('R', 0, tmp_u)
        cube.set_row('Y', 0, tmp_r, reverse=True)
        cube.set_col('O', 2, tmp_d)
        cube.set_row('W', 2, tmp_l, reverse=True)

    elif direction == "B":
        cube.rotate_face('B')
        tmp_u = cube.get_row('W', 0)
        tmp_r = cube.get_col('O', 2)
        tmp_d = cube.get_row('Y', 2)
        tmp_l = cube.get_col('R', 0)
        cube.set_col('O', 0, tmp_u, reverse=True)
        cube.set_row('Y', 2, tmp_r)
        cube.set_col('R', 2, tmp_d, reverse=True)
        cube.set_row('W', 0, tmp_l)

    # Direction R(Red), L(Orange) - C C C C
    elif direction == "R":
        cube.rotate_face('R')
        tmp_u = cube.get_col('W', 2)
        tmp_r = cube.get_col('B', 0)
        tmp_d = cube.get_col('Y', 2)
        tmp_l = cube.get_col('G', 2)
        cube.set_col('B', 0, tmp_u, reverse=True)
        cube.set_col('Y', 2, tmp_r, reverse=True)
        cube.set_col('G', 2, tmp_d)
        cube.set_col('W', 2, tmp_l)

    elif direction == "L":
        cube.rotate_face('O')
        tmp_u = cube.get_col('W', 0)
        tmp_r = cube.get_col('G', 0)
        tmp_d = cube.get_col('Y', 0)
        tmp_l = cube.get_col('B', 2)
        cube.set_col('G', 0, tmp_u)
        cube.set_col('Y', 0, tmp_r)
        cube.set_col('B', 2, tmp_d, reverse=True)
        cube.set_col('W', 0, tmp_l, reverse=True)

    # Direction U(White), D(Yellow) - R R R R
    elif direction == "U":
        cube.rotate_face('W')
        tmp_u = cube.get_row('O', 0)
        tmp_r = cube.get_row('B', 0)
        tmp_d = cube.get_row('R', 0)
        tmp_l = cube.get_row('G', 0)
        cube.set_row('B', 0, tmp_u)
        cube.set_row('R', 0, tmp_r)
        cube.set_row('G', 0, tmp_d)
        cube.set_row('O', 0, tmp_l)

    elif direction == "D":
        cube.rotate_face('Y')
        tmp_u = cube.get_row('G', 2)
        tmp_r = cube.get_row('R', 2)
        tmp_d = cube.get_row('B', 2)
        tmp_l = cube.get_row('O', 2)
        cube.set_row('R', 2, tmp_u)
        cube.set_row('B', 2, tmp_r)
        cube.set_row('O', 2, tmp_d)
        cube.set_row('G', 2, tmp_l)

    return cube


if __name__ == "__main__":
    main()
