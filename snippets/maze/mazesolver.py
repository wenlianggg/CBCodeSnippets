# Wen Liang Goh - https://github.com/wenlianggg
# 1 May 2020
# Maze solver
# Only 1 entry and 1 exit allowed in this version
# Save maze to mazefile.txt, solves and generates graph in graph.png
# Using NetworkX for weighted graph searching

import networkx as nx
try:  # Try and import optional dependencies
    import matplotlib.pyplot as plt
    from matplotlib import colors
    import numpy as np
except ImportError:
    plt = None
    colors = None
    np = None

WALL_CHAR = '.'
SPACE_CHAR = '0'
maze = []
intersect_list = []
entryexitcoords = []

graph = nx.Graph()

with open('mazefile.txt', 'r') as file:
    lines = file.readlines()

for lineidx in range(len(lines)):
    lines[lineidx] = lines[lineidx].replace('\n', '')
    maze.append([])
    for char in lines[lineidx]:
        maze[lineidx].append(char)

rows = len(maze)
cols = len(maze[0])

# Scan for entry/exit point
firstrow, lastrow = maze[0], maze[-1]
firstcol, lastcol = [item[0] for item in maze], [item[-1] for item in maze]

for idx in range(cols):
    if firstrow[idx] == SPACE_CHAR:
        entryexitcoords.append([idx, 0])
    if lastrow[idx] == SPACE_CHAR:
        entryexitcoords.append([idx, rows - 1])

for idx in range(rows):
    if firstcol[idx] == SPACE_CHAR:
        entryexitcoords.append([0, idx])
    if lastcol[idx] == SPACE_CHAR:
        entryexitcoords.append([cols - 1, idx])

print("Entry/exit points:", *entryexitcoords)
entry_iidx = 0
exit_iidx = 0

# Loop through and find all intersections
for y in range(rows):
    for x in range(cols):

        if maze[y][x] == SPACE_CHAR:

            if [x, y] == entryexitcoords[0]:
                intersect_list.append([x, y])
                entryiidx = intersect_list.index([x, y])
                continue

            if [x, y] == entryexitcoords[1]:
                intersect_list.append([x, y])
                exit_iidx = intersect_list.index([x, y])
                continue

            if maze[y + 1][x] == SPACE_CHAR and maze[y - 1][x] == SPACE_CHAR and not maze[y][x + 1] == SPACE_CHAR and not maze[y][x - 1] == SPACE_CHAR:
                continue  # Up and down is the same lol
            elif maze[y][x + 1] == SPACE_CHAR and maze[y][x - 1] == SPACE_CHAR and not maze[y + 1][x] == SPACE_CHAR and not maze[y - 1][x] == SPACE_CHAR:
                continue  # Left and right is the same lol

            turningpoints = 0
            if maze[y + 1][x] == SPACE_CHAR:
                turningpoints += 1
            elif maze[y - 1][x] == SPACE_CHAR:
                turningpoints += 1
            if maze[y][x + 1] == SPACE_CHAR:
                turningpoints += 1
            elif maze[y][x - 1] == SPACE_CHAR:
                turningpoints += 1
            if turningpoints > 1:
                intersect_list.append([x, y])

# Add all intersections as nodes in graph
graph.add_nodes_from(range(len(intersect_list)))

# Look around this intersection for walls/other intersections (RIGHT, DOWN, LEFT, UP)
for fromX, fromY in intersect_list:
    from_index = intersect_list.index([fromX, fromY])

    # Dont look around if its the exit lol
    if from_index == exit_iidx:
        break

    for direction in range(4):
        for i in range(1, 1000):
            # Set the coordinates to look at
            if direction == 0:
                x, y = fromX - i, fromY
            elif direction == 1:
                x, y = fromX, fromY + i
            elif direction == 2:
                x, y = fromX + i, fromY
            elif direction == 3:
                x, y = fromX, fromY - i

            # Perform looking
            try:
                if maze[y][x] == WALL_CHAR:  # Break upon encountering a wall
                    break
                elif [x, y] in intersect_list:
                    other_intersect_idx = intersect_list.index([x, y])
                    graph.add_edge(from_index, other_intersect_idx, weight=i)
                    break
                elif maze[y][x] == SPACE_CHAR:
                    continue
            except Exception:
                print("Error while reading maze", from_index)
                break

# Find the shortest path
try:
    shortestpath = nx.shortest_path(graph, entry_iidx, exit_iidx)
    print("Shortest path: ", *shortestpath)
except nx.exception.NetworkXNoPath:
    print("Path not found!")
    shortestpath = []


# Mark out path of the shortest route
leftpaths, rightpaths, downpaths, uppaths = [[] for i in range(4)]
for intersect_idx in range(len(shortestpath) - 1):
    thisX, thisY = intersect_list[shortestpath[intersect_idx]]
    destX, destY = intersect_list[shortestpath[intersect_idx + 1]]
    for i in range(max(rows, cols)):
        if thisX + i - destX < 0:  # Moving right
            rightpaths.append([thisX + i, thisY])
        elif thisX - i - destX > 0:  # Moving left
            leftpaths.append([thisX - i, thisY])
        elif thisY - destY + i < 0:  # Moving down
            downpaths.append([thisX, thisY + i])
        elif thisY - destY - i > 0:  # Moving up
            uppaths.append([thisX, thisY - i])


# Optional dependency check
if np and plt and colors:
    plotdata = []
    for y in range(rows):
        xarray = []
        for x in range(cols):
            if [x, y] in entryexitcoords:
                xarray.append(20.0)
            elif any([x, y] in path for path in [leftpaths, rightpaths, downpaths, uppaths]):
                xarray.append(10.0)
            elif maze[y][x] == SPACE_CHAR:
                xarray.append(0.0)
            elif maze[y][x] == WALL_CHAR:
                xarray.append(30.0)
            else:
                xarray.append(40.0)
        plotdata.append(xarray)
    nparray = np.asarray(plotdata)

    cmap = colors.ListedColormap(['white', 'lightgreen', 'blue', 'black'])
    bounds = [0, 10, 20, 30, 40]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    fig, ax = plt.subplots()
    fig.canvas.set_window_title('Maze Solver')
    ax.imshow(nparray, cmap=cmap, norm=norm)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    # draw gridlines
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(False)
    plt.savefig("mazesolved.png", bbox_inches='tight', pad_inches=0, dpi=200)
    plt.show()
    nx.draw(graph, with_labels=True)
    plt.savefig("graph.png")

# Print maze with corners
for y in range(rows):
    for x in range(cols):
        # Print intersection IDs
        # if [x, y] in intersect_list:
        #    intersect_idx = intersect_list.index([x, y])
        #    print("{:02d}".format(intersect_idx), end='')
        if [x, y] in leftpaths:
            print('← ', end='')
        elif [x, y] in rightpaths:
            print('→ ', end='')
        elif [x, y] in uppaths:
            print('↑ ', end='')
        elif [x, y] in downpaths:
            print('↓ ', end='')
        # elif [x, y] == entry:
        #     print('@@', end='')
        # elif [x, y] == exit:
        #     print('##', end='')
        elif maze[y][x] == SPACE_CHAR:
            print('  ', end='')
        elif maze[y][x] == WALL_CHAR:
            print('██', end='')
        else:
            print('XX', end='')
    print()
