# Wen Liang Goh - https://github.com/wenlianggg
# 3 April 2020
# Transforms a matrix to RREF form.


def main():
    # rows = [
    #     [0,-3,2,-2],
    #     [0,2,2,-2]
    # ]
    # n_rows = len(rows)

    rows = []
    n_rows = int(input("Enter the number of rows: ").strip())

    for i in range(n_rows):
        userinput = input(f"Enter row {i} separated by space: ").strip()
        rows.append([float(r) for r in userinput.split(' ')])

    n_cols = len(rows[0])

    print_rows(rows, "Your input...")
    print("--- Starting to solve ---")

    currentPivotRow = 0
    for colN in range(n_cols):
        done = solve_col(rows, n_rows, colN, currentPivotRow)
        if done:
            currentPivotRow += 1

    print_rows(rows, "Final Answer")


# Solve the column
def solve_col(rows, n_rows, colN, pivotRow):
    non_pivot_rows = [i for i in range(n_rows) if i != pivotRow]

    all_in_col = [row[colN] for row in rows if row[colN] != 0]
    if len(all_in_col) == 0:
        print("Skipping column", colN)
        return False

    if pivotRow >= len(rows):
        return False

    if rows[pivotRow][colN] == 0:
        for rowN in non_pivot_rows:
            if rows[pivotRow][colN] != 0:
                temp_row = rows[colN]
                rows[colN] = rows[rowN]
                rows[rowN] = temp_row
                print_rows(rows, f'SWAPPING - R{colN} <-> R{rowN}')
                break

    # make the pivot 1
    msg = f'MAKING PIVOT ONE - R{pivotRow} / {rows[pivotRow][colN]}'
    if rows[pivotRow][colN] != 1:
        rows[pivotRow] = [i / rows[pivotRow][colN] for i in rows[pivotRow]]
    print_rows(rows, msg)

    for rowN in non_pivot_rows:
        # make all in column 0 to 0 except for first row
        multiple = rows[rowN][colN] / rows[pivotRow][colN]
        msg = f'ZEROING NON-PIVOT R{rowN} * {multiple}'
        for i in range(len(rows[rowN])):
            rows[rowN][i] = rows[rowN][i] - rows[pivotRow][i] * multiple
        print_rows(rows, msg)

    print(f'--- Column {colN} solved ---')
    return True


def print_rows(rows, comment=''):
    print(comment)
    for row in rows:
        for i in row:
            print("{:.3f}\t".format(i + 0), end='')
        print()


if __name__ == "__main__":
    main()
