from csp import backtrack

def print_board(assignment):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            val = assignment.get((i, j), 0)
            print(val if val != 0 else ".", end=" ")
        print()
    print()

def build_csp(board):
    variables = []
    domain = {}
    neighbors = {}

    for i in range(9):
        for j in range(9):
            cell = (i, j)
            variables.append(cell)

            # domain
            if board[i][j] != 0:
                domain[cell] = [board[i][j]]
            else:
                domain[cell] = list(range(1, 10))

            neighbors[cell] = set()

    # constraints
    for i in range(9):
        for j in range(9):
            cell = (i, j)

            # row + column
            for k in range(9):
                if k != j:
                    neighbors[cell].add((i, k))
                if k != i:
                    neighbors[cell].add((k, j))

            # box
            sr, sc = (i // 3) * 3, (j // 3) * 3
            for r in range(sr, sr + 3):
                for c in range(sc, sc + 3):
                    if (r, c) != cell:
                        neighbors[cell].add((r, c))

    return variables, domain, neighbors

#sample board (0 = empty)
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],

    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],

    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

print("Unsolved Sudoku:\n")

initial_assignment = {}
for i in range(9):
    for j in range(9):
        if board[i][j] != 0:
            initial_assignment[(i, j)] = board[i][j]

print_board(initial_assignment)

variables, domain, neighbors = build_csp(board)

solution = backtrack(variables, domain, neighbors, {})

if solution:
    print("Solved Sudoku:\n")
    print_board(solution)
else:
    print("No solution found.")