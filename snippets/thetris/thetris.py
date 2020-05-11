import threading
import msvcrt
import sys
import random

TICK_TIME_MILLIS = 500
GAME_HEIGHT = 16
GAME_WIDTH = 10
KEYMAP = { 72: 'U', 75: 'L', 80: 'D', 77: 'R', 0: '-' }
BLOCK_CTR = { 'I': 0, 'J': 0, 'L': 0, 'O': 0, 'S': 0, 'T': 0, 'Z': 0 }
BLOCK_BASE = { 'I': 1000, 'J': 2000, 'L': 3000, 'O': 4000, 'S': 5000, 'T': 6000, 'Z': 7000 }
(   GAME_VALID, GAME_STARTED, GAME_OVER, 
    BLOCK_INSERT_OK, BLOCK_MOVE_OK, BLOCK_MOVE_FAIL,
    BLOCK_BOTTOMED, USER_MOVED
) = range(8)

def main():
    grid = []
    direction = 'D'
    curr_block_id = None
    curr_block_type = None
    next_block_id = None
    next_block_type = None
    game_state = GAME_STARTED

    for _ in range(GAME_HEIGHT):
        grid.append([0, ] * GAME_WIDTH)

    while game_state is not GAME_OVER:  # Game tick
        print("Game State =", game_state)
        if game_state == BLOCK_MOVE_OK or game_state == BLOCK_INSERT_OK:
            game_state = grid_block_move(grid, curr_block_id, direction='D')
        
        elif game_state == USER_MOVED:
            game_state = grid_block_move(grid, curr_block_id, direction=direction)

        elif game_state == BLOCK_BOTTOMED:
            curr_block_id, curr_block_type = next_block_id, next_block_type 
            next_block_id, next_block_type = get_next_block()
            game_state = grid_insert_block(grid, blocktype=curr_block_type, blockid=curr_block_id)

        elif game_state == GAME_STARTED:
            curr_block_id, curr_block_type = get_next_block()
            next_block_id, next_block_type = get_next_block()
            game_state = grid_insert_block(grid, blocktype=curr_block_type, blockid=curr_block_id)

        if game_state == GAME_OVER:
            print("Game over...")
            return

        displaygame(grid=grid, curr=curr_block_type, next=next_block_type)
        print(game_state)

        usermove = readInput('Entered move', 'D', TICK_TIME_MILLIS)

        if usermove is not 0:
            game_state = USER_MOVED
            direction = KEYMAP[usermove]
            print(direction)
        else:
            direction = 'D'

def displaygame(grid: list, curr: str, next: str):
    for i in range(GAME_HEIGHT):
        print("|", end='')
        for item in grid[i]:
            if item == 0:
                print(f'[    ]', end='')
            else:
                print(f'[{item:04d}]', end='')
        print("|", end='')
        if i == 3:
            print("    Current Block", end='')
        if i == 4:
            print("   ", curr, end='')
        if i == 5:
            print("    Next Piece", end='')
        if i == 6:
            print("   ", next, end='')
        print()
    print(" ⁠—⁠—⁠—⁠—⁠—⁠—⁠—⁠—⁠—⁠— \n")

def get_next_block():
    blocktypes_avail = list(BLOCK_CTR.keys())
    blocktype = random.choice(blocktypes_avail)
    blockid = BLOCK_BASE[blocktype] + (BLOCK_CTR[blocktype] % 1000 + 1)
    BLOCK_CTR[blocktype] += 1 # Increment counter to prevent ID collision
    return blockid, blocktype

def grid_block_move(grid, blockid: int, direction):
    block_locations = []
    new_locations = []
    print("Trying to move:", direction)
    for y in range(GAME_HEIGHT):
        for x in range(GAME_WIDTH):
            if grid[y][x] == blockid:

                if y + 1 >= GAME_HEIGHT:
                    print("Block bottomed on the base")
                    return BLOCK_BOTTOMED

                thiscoord = [x, y]
                newcoord = [None, None]
                
                # Identify new coordinates for respective movement
                if direction == 'L':
                    newcoord = [thiscoord[0] - 1, thiscoord[1]]
                if direction == 'D':
                    newcoord = [thiscoord[0], thiscoord[1] + 1]
                if direction == 'R':
                    newcoord = [thiscoord[0] + 1, thiscoord[1]]

                if direction in ['L', 'D', 'R'] and (grid[newcoord[1]][newcoord[0]] == 0 or grid[newcoord[1]][newcoord[0]] == blockid):
                    block_locations.append(thiscoord)
                    new_locations.append(newcoord)
                else:
                    print("Block bottomed on another tile")
                    return BLOCK_BOTTOMED

    for x, y in block_locations:
        grid[y][x] = 0

    for x, y in new_locations:
        grid[y][x] = blockid

    return BLOCK_MOVE_OK

def grid_insert_block(grid, blocktype: str, blockid: int):
    # Inserts into default position (centered on [1][4] and [1][5])
    print(blocktype, blockid)
    if grid[1][4] == 0 and grid[1][5] == 0:  # Checks default (common) position for filled
        # Check type-specific locations
        if blocktype == 'I' and grid[1][3] == 0 and grid[1][6] == 0:
            grid[1][4] = grid[1][5] = grid[1][3] = grid[1][6] = blockid
            return BLOCK_INSERT_OK
        elif blocktype == 'J' and grid[1][3] == 0 and grid[0][3] == 0:
            grid[1][4] = grid[1][5] = grid[1][3] = grid[0][3] = blockid
            return BLOCK_INSERT_OK
        elif blocktype == 'L' and grid[1][3] == 0 and grid[0][5] == 0:
            grid[1][4] = grid[1][5] = grid[1][3] = grid[0][5] = blockid
            return BLOCK_INSERT_OK
        elif blocktype == 'O' and grid[0][4] == 0 and grid[0][5] == 0:
            grid[1][4] = grid[1][5] = grid[0][4] = grid[0][5] = blockid
            return BLOCK_INSERT_OK
        elif blocktype == 'S' and grid[1][3] == 0 and grid[0][4]  == 0 and grid[0][5] == 0:
            grid[1][3] = grid[1][4] = grid[0][4] = grid[0][5] = blockid
            return BLOCK_INSERT_OK
        elif blocktype == 'T' and grid[1][3] == 0 and grid[0][4] == 0:
            grid[1][4] = grid[1][5] = grid[1][3] = grid[0][4] = blockid
            return BLOCK_INSERT_OK
        elif blocktype == 'Z' and grid[0][3] == 0 and grid[0][4] == 0:
            grid[1][4] = grid[1][5] = grid[0][3] = grid[0][4] = blockid
            return BLOCK_INSERT_OK
        elif blocktype is None:
            print("No new tile provided")
            return BLOCK_INSERT_OK
        else:
            print("No space to insert specific new tile")
            return GAME_OVER
    else:
        print("No space to insert any new tile")
        return GAME_OVER

# Utility Functions
def readInput(caption, default, timeout):
    class KeyboardThread(threading.Thread):
        def run(self):
            self.timedout = False
            self.input = 0
            while not self.timedout:
                if msvcrt.kbhit():
                    chr = msvcrt.getche()
                    self.input = ord(chr)
                    return

    #print(f"{caption}: ", end='')
    result = default
    try:
        kb_thread = KeyboardThread()
        kb_thread.start()
        kb_thread.join(timeout / 1000)
        kb_thread.timedout = True
        kb_thread.join()
    except (KeyboardInterrupt, SystemExit):
        print('Quitting\n')
    result = kb_thread.input
    return result

if __name__ == "__main__":
    main()