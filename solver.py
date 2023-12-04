def solve(board):
    find = find_empty(board) # checks for empty cells
    if not find: # if none empty, board is already solved
        return True
    else:
        row, col = find

    # simple backtracking algorithm to solve the board
    for i in range(1,10):
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False


def valid(board, num, pos):
    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    x = pos[1] // 3
    y = pos[0] // 3

    # check 3x3 boxes
    for i in range(y*3, y*3 + 3):
        for j in range(x * 3, x*3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False

    return True

# terminal visualization of board
def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

# checks for empty cells
def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col

    return None