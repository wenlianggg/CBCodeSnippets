
gridx, gridy = 4, 4
straightctr, diagctr = 0, 0
coords = [[x, y] for x in range(gridx) for y in range(gridy)]

for x1, y1 in coords:
    for x2, y2 in coords:
        if x2 - x1 > 0 and y2 - y1 > 0:
            print(f"S: {x1},{y1} to {x2},{y2} - {x2-x1}x{y2-y1}")
            straightctr += 1
        if x2 - x1 > 1 and y2 - y1 > 1 and x2 - x1 == y2 - y1:
            print(f"D: {x1},{y1} to {x2},{y2} - {x2-x1}x{y2-y1}")
            diagctr += 1

print("Upright quadrilaterals", straightctr)
print("Diagonal quadrilaterals", diagctr)
