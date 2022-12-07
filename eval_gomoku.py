import copy
# value output for five in a row
fivewin = 100000

board_size = 8
empty = 0
taken = 3
black = 1
white = 2

# stone patterns
fiverow = [1,1,1,1,1]
open4 = [[0,1,1,1,1,0],[-1,1,1,0,1,0,1,1,1,-1],[-1,1,1,0,1,0,1,1,1,-1]]
simp4 = [[-1,1,1,1,1,0],[0,1,1,1,1,-1],[1,1,0,1,1]]
open3 = [[0,0,1,1,1,0,0],[0,1,0,1,1,0,1,0],[1,0,1,0,1,0,1,0,1]]
broken3 = [[0,1,1,0,1,0],[0,1,0,1,1,0],[-1,0,1,1,1,0,0],[0,0,1,1,1,0,-1]]
simp3 = [[-1,1,1,1,0,0],[0,0,1,1,1,-1]]
simp2 = [[-1,1,1,0,0,0],[0,0,0,1,1,-1],[0,0,1,1,0],[0,1,1,0,0]]

patterns = [open4, simp4, open3,broken3,simp3,simp2]
# winning value for each pattern
winning = [2000, 1000, 800, 400, 50, 10]

# get the full row, column and two diagonals of a position
def getRows(board, pos):
    row = board[pos[0]]
    col = [row[pos[1]] for row in board]
    diag1 = []
    diag2 = []
    if pos[0] == max(pos):
        j = 0
        for i in range(pos[0] - pos[1], board_size):
            diag1.append(board[i][j])
            j += 1
        if pos[0] >= board_size - pos[1]:
            j = board_size - 1
            for i in range(pos[0] - (board_size - 1 - pos[1]), board_size):
                diag2.append(board[i][j])
                j -= 1
        else:
            i = 0
            for j in range(pos[0] + pos[1], -1, -1):
                diag2.append(board[i][j])
                i += 1
    else:
        j = pos[1] - pos[0]
        for i in range(0, board_size - pos[1] + pos[0]):
            diag1.append(board[i][j])
            j += 1

        if pos[0] >= board_size - pos[1]:
            j = board_size - 1
            for i in range(pos[0] - (board_size - 1 - pos[1]), board_size):
                diag2.append(board[i][j])
                j -= 1
        else:
            i = 0
            for j in range(pos[0] + pos[1], -1, -1):
                diag2.append(board[i][j])
                i += 1
    return [row, col, diag1, diag2]


# translate the given board row to match the notation used in stone patterns
def pattern(row,cur):
    res = []
    for i in row:
        if i == cur:
            res.append(1)
        elif i == empty:
            res.append(0)
        else:
            res.append(-1)
    return res

# evaluation function
def eval(board, cur, pos):
    temp = copy.deepcopy(board)
    temp[pos[0]][pos[1]] = cur
    adv = white if cur == black else black
    # first gets the 4 "rows" of a position
    checks = getRows(temp,pos)

    # determining how much advantage it will gain playing here
    winning_checks = [pattern(i, cur) for i in checks]
    winning_value = threat(winning_checks)
    # determining how much threat eliminated playing here
    threat_checks = [pattern(i, adv) for i in checks]
    threat_value = threat(threat_checks)

    # if encountering a five in a row situation
    # this position must be taken, directly return
    if(winning_value == fivewin or threat_value == fivewin):
        return fivewin

    # else adding the advantage and threat elimination value together
    winning_val = sum(i[0] * i[1] for i in zip(winning, winning_value))
    winning_val += sum(i[0] * i[1] for i in zip(winning, threat_value))
    return winning_val


def threat(checks):
    count_list = []
    # check if there is a five-in-a-row case
    for check in checks:
        for i in range(len(check) - len(fiverow) + 1):
            if check[i: i + len(fiverow)] == fiverow:
                return fivewin

    # check all the other patterns
    for pat in patterns:
        res = 0
        for type in pat:
            for check in checks:
                for i in range(len(check) - len(type) + 1):
                    if check[i: i + len(type)] == type:
                        res += 1
                        break
        count_list.append(res)
    return count_list

# find an empty space that is close to the given position
def findempty(board,pos):
    for i in range(board_size):
        upper = pos[0] + i if pos[0] + i < board_size else board_size-1
        lower = pos[0] - i if pos[0] - i >= 0 else 0
        right = pos[1] + i if pos[1] + i < board_size else board_size-1
        left = pos[1] - i if pos[1] - i >= 0 else 0
        if board[upper][pos[1]] == empty:
            return [upper,pos[1]]
        if board[lower][pos[1]] == empty:
            return [lower, pos[1]]
        if board[pos[0]][left] == empty:
            return [pos[0],left]
        if board[pos[0]][right] == empty:
            return [pos[0], right]
        if board[upper][left] == empty:
            return [upper,left]
        if board[upper][right] == empty:
            return [upper, right]
        if board[lower][left] == empty:
            return [lower,left]
        if board[lower][right] == empty:
            return [lower, right]


# find the position that will give the max value
# that is within the check_size range
def findMax(board, cur,pos,check_size):
    # if board already full, return 0
    if all (all(j != 0 for j in i) for i in board):
        return 0

    # define the range
    upper = pos[0] + check_size if pos[0] + check_size < board_size else board_size
    lower = pos[0] - check_size if pos[0] - check_size >= 0 else 0
    right = pos[1] + check_size if pos[1] + check_size < board_size else board_size
    left = pos[1] - check_size if pos[1] - check_size >= 0 else 0
    maxval = 0
    bestpos = []
    # loop within this range and find the best position
    for i in range(lower, upper):
        for j in range(left, right):
            if board[i][j] == 0:
                val = eval(board, cur, [i, j])
                if val > fivewin:
                    return [i,j]
                if val > maxval:
                    bestpos = [i,j]
                    maxval = val
                # print("position %d %d val = %d" % (i, j, val))

    # if all position is of the same value, find the closest empty
    # space to the previous opponent's move
    if not bestpos:
        return findempty(board, pos)

    return bestpos

# check if there is five in a row
def check_five(row):
    for i in range(len(row)-4):
        if row[i] == row[i+1] and row[i] == row[i+2] and row[i] == row[i+3] and row[i] == row[i+4]:
            return row[i]
    return 0

# check who is the winner
def check_winner(board):
    for i in range(board_size):
        checks = [getRows(board, [i, i]),getRows(board, [0, i]),getRows(board, [i, 0])]
        for check in checks:
            for row in check:
                ret = check_five(row)
                if ret != 0:
                    return ret
    return 0


# display the board
def display_board(board):
    print("-"*(board_size*2+1))
    for i in range(board_size):
        print("|",end="")
        for j in range(board_size):
            if board[i][j] == black:
                print("b",end="|")
            elif board[i][j]== white:
                print("w",end="|")
            else:
                print(" ",end="|")
        print("\n" + "-" * (board_size * 2+1))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # board = [[0,0,0,0,0,0,0,0],
    #             [0,0,0,0,0,0,0,0],
    #             [0,0,1,2,1,0,0,0],
    #             [0,0,1,2,2,2,0,0],
    #             [0,0,1,2,1,0,0,0],
    #             [0,0,1,0,1,0,0,0],
    #             [0,0,0,0,0,0,0,0],
    #             [0,0,0,0,0,0,0,0]]
    # print(check_winner(board))
    cur = white
    board = [[0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 2, 1, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 2, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0]]
    check_size = 4
    pos = [5, 2]
    while check_winner(board) == 0:
        cur = white if cur == black else black
        pos = findMax(board, white, pos, check_size)
        if not pos:
            break
        board[pos[0]][pos[1]] = cur
        # display_board(board)
    display_board(board)
    if pos == 0:
        print("Tied")
    else:
        winner = "black" if check_winner(board) == black else "white"
        print("winner is %s" %winner)


