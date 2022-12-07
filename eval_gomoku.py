# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
checking = 3
fivewin = 100000
board_size = 8
empty = 0
taken = 3
black = 1
white = 2
fiverow = [1,1,1,1,1]
open4 = [[0,1,1,1,1,0],[-1,1,1,0,1,0,1,1,1,-1],[-1,1,1,0,1,0,1,1,1,-1]]
simp4 = [[-1,1,1,1,1,0],[0,1,1,1,1,-1],[1,1,0,1,1]]
open3 = [[0,0,1,1,1,0,0],[0,1,0,1,1,0,1,0],[1,0,1,0,1,0,1,0,1]]
broken3 = [[0,1,1,0,1,0],[0,1,0,1,1,0],[-1,0,1,1,1,0,0],[0,0,1,1,1,0,-1]]
# open3s = [[0,1,1,1,0]]
simp3 = [[-1,1,1,1,0,0],[0,0,1,1,1,-1]]
simp2 = [[0,1,1,0,0,0],[0,0,1,1,0,0],[0,0,0,1,1,0]]


patterns = [open4, simp4, open3,broken3,simp3,simp2]

winning = [2000, 1000, 800, 400, 200, 10, 5]

# 00 01 02 03 04
# 10 11 12 13 14
# 20 21 22 23 24
# 30 31 32 33 34
# 40 41 42 43 44
import copy

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



def eval(board, cur, pos):
    temp = copy.deepcopy(board)
    temp[pos[0]][pos[1]] = cur
    adv = white if cur == black else black
    checks = getRows(temp,pos)
    # pattern(row,cur), pattern(col,cur), pattern(diag1,cur), pattern(diag2,cur)
    # checks = [row, col, diag1, diag2]
    winning_checks = [pattern(i, cur) for i in checks]
    threat_checks = [pattern(i, adv) for i in checks]

    winning_value = threat(winning_checks)
    threat_value = threat(threat_checks)
    if(winning_value == fivewin or threat_value == fivewin):
        return fivewin
    # print(threat_value,winning_value)
    winning_val = sum(i[0] * i[1] for i in zip(winning, winning_value))
    winning_val += sum(i[0] * i[1] for i in zip(winning, threat_value))
    return winning_val


def threat(checks):
    bool_list = []

    for check in checks:
        for i in range(len(check) - len(fiverow) + 1):
            if check[i: i + len(fiverow)] == fiverow:
                return fivewin

    for pat in patterns:
        res = 0
        for type in pat:
            for check in checks:
                for i in range(len(check) - len(type) + 1):
                    if check[i: i + len(type)] == type:
                        res += 1
                        break
        bool_list.append(res)
    return bool_list
    # return sum(i[0] * i[1] for i in zip(value_list, bool_list))

def findMax(board, cur,upper, lower, left, right):
    maxval = 0
    bestpos = []
    for i in range(lower, upper):
        for j in range(left, right):
            if board[i][j] == 0:
                val = eval(board, cur, [i, j])
                if val > fivewin:
                    return [i,j]
                if val >= maxval:
                    bestpos = [i,j]
                    maxval = val
                # print("position %d %d val = %d" % (i, j, val))
    return bestpos

def check_five(row):
    for i in range(len(row)-4):
        if row[i] == row[i+1] and row[i] == row[i+2] and row[i] == row[i+3] and row[i] == row[i+4]:
            return row[i]
    return 0


def check_winner(board):
    for i in range(board_size):
        for j in range(board_size):
            checks = getRows(board,[i,j])
            for check in checks:
                ret = check_five(check)
                if ret != 0:
                    return ret
    return 0

def simple(board,check_size,pos,cur):
    size = len(board)
    upper = pos[0] + check_size if pos[0] + check_size < size else size
    lower = pos[0] - check_size if pos[0] - check_size >= 0 else 0
    right = pos[1] + check_size if pos[1] + check_size < size else size
    left = pos[1] - check_size if pos[1] - check_size >= 0 else 0
    ret = findMax(board,cur,upper,lower,left,right)
    return ret


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
    cur = black
    board = [[0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 2, 1, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 2, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0]]
    check_size = 3
    pos = [5, 2]
    while check_winner(board) == 0:
        # print(board)
        cur = white if cur == black else black
        upper = pos[0] + check_size if pos[0] + check_size < board_size else board_size
        lower = pos[0] - check_size if pos[0] - check_size >= 0 else 0
        right = pos[1] + check_size if pos[1] + check_size < board_size else board_size
        left = pos[1] - check_size if pos[1] - check_size >= 0 else 0
        pos = findMax(board, white, upper, lower, left, right)
        if not pos:
            print(eval(board,cur,))
        board[pos[0]][pos[1]] = cur
        display_board(board)
    winner = "black" if check_winner(board) == black else "white"
    print("winner is %s" %winner)


