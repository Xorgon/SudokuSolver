import numpy as np
import math

sudoku = np.zeros([9, 9], dtype=list)


def deserialize_sudoku(serialized):
    """
    a b c d e f g h i
    j k l . . . . . .
    . . . . . . . . .

    would be from

    abcdefghijkl...
    """
    serialized = serialized.replace(",", "")
    if len(serialized) != 9*9:
        print("Wrong length")
        print(9*9 - len(serialized))
        return False
    deserialized = np.zeros([9, 9], dtype=list)
    for i in range(9):
        for j in range(9):
            val = int(serialized[9*j + i])
            if val == 0:
                deserialized[i, j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            else:
                deserialized[i, j] = val
    return deserialized


def test_square(i, j, sudoku):
    sqr_x = math.modf(i/3.)[1]
    sqr_y = math.modf(j/3.)[1]
    for dif_i in range(3):
        cur_i = 3 * sqr_x + dif_i
        for dif_j in range(3):
            cur_j = 3 * sqr_y + dif_j
            if cur_i == i and cur_j == j:
                continue
            elif not type(sudoku[cur_i, cur_j]) is list:
                val = int(sudoku[cur_i, cur_j])
                if sudoku[i, j].count(val) > 0:
                    sudoku[i, j].remove(val)
    return sudoku


def test_horiz(i, j, sudoku):
    for cur_i in range(9):
        if cur_i == i:
            continue
        elif not type(sudoku[cur_i, j]) is list:
            val = int(sudoku[cur_i, j])
            if sudoku[i, j].count(val) > 0:
                sudoku[i, j].remove(val)
    return sudoku


def test_vert(i, j, sudoku):
    for cur_j in range(9):
        if cur_j == j:
            continue
        elif not type(sudoku[i, cur_j]) is list:
            val = int(sudoku[i, cur_j])
            if sudoku[i, j].count(val) > 0:
                sudoku[i, j].remove(val)
    return sudoku


def test_row(j, sudoku):
    rem_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(9):
        if type(sudoku[i, j]) is not list:
            rem_vals.remove(sudoku[i, j])
    for val in rem_vals:
        poss = []
        for i in range(9):
            if type(sudoku[i, j]) is list and sudoku[i, j].count(val) > 0:
                poss.append(i)
        if len(poss) == 1:
            sudoku[poss[0], j] = val
    return sudoku


def test_column(i, sudoku):
    rem_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for j in range(9):
        if type(sudoku[i, j]) is not list:
            rem_vals.remove(sudoku[i, j])
    for val in rem_vals:
        poss = []
        for j in range(9):
            if type(sudoku[i, j]) is list and sudoku[i, j].count(val) > 0:
                poss.append(j)
        if len(poss) == 1:
            sudoku[i, poss[0]] = val
    return sudoku


def test_3x3(x, y, sudoku):
    rem_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i_mod in range(3):
        for j_mod in range(3):
            i = 3 * x + i_mod
            j = 3 * y + j_mod
            if type(sudoku[i, j]) is not list:
                rem_vals.remove(sudoku[i, j])
    for val in rem_vals:
        poss = []
        for i_mod in range(3):
            for j_mod in range(3):
                i = 3 * x + i_mod
                j = 3 * y + j_mod
                if type(sudoku[i, j]) is list and sudoku[i, j].count(val) > 0:
                    poss.append((i, j))
        if len(poss) == 1:
            sudoku[poss[0]] = val
    return sudoku


def output(sudoku):
    string = ""
    for j in range(9):
        for i in range(9):
            if type(sudoku[i, j]) is list:
                string += "_ "
            else:
                string += str(sudoku[i, j]) + " "
            if i == 8:
                string += "\n"
    print(string)


def count_spaces(sudoku):
    count = 0
    for i in range(9):
        for j in range(9):
            if type(sudoku[i, j]) is list:
                count += 1
    return count


def test_valid_row(j, sudoku):
    contains = []
    for i in range(9):
        if type(sudoku[i, j]) is not list:
            if contains.count(sudoku[i, j]) > 0:
                return False
            else:
                contains.append(sudoku[i, j])
    return True


def test_valid_column(i, sudoku):
    contains = []
    for j in range(9):
        if type(sudoku[i, j]) is not list:
            if contains.count(sudoku[i, j]) > 0:
                return False
            else:
                contains.append(sudoku[i, j])
    return True


def test_valid_3x3(x, y, sudoku):
    contains = []
    for i_mod in range(3):
        for j_mod in range(3):
            i = 3 * x + i_mod
            j = 3 * y + j_mod
            if type(sudoku[i, j]) is not list:
                if contains.count(sudoku[i, j]) > 0:
                    return False
                else:
                    contains.append(sudoku[i, j])
    return True


def test_valid(sudoku):
    for i in range(9):
        if not test_valid_column(i, sudoku):
            return False
    for j in range(9):
        if not test_valid_row(j, sudoku):
            return False
    for x in range(3):
        for y in range(3):
            if not test_valid_3x3(x, y, sudoku):
                return False
    return True


def solve(sudoku):
    output(sudoku)
    iteration = 0
    while count_spaces(sudoku) > 0:
        print(iteration)
        iteration += 1
        # Testing possible values of each cell.
        for i in range(9):
            for j in range(9):
                if type(sudoku[i, j]) is list:
                    sudoku = test_square(i, j, sudoku)
                    sudoku = test_horiz(i, j, sudoku)
                    sudoku = test_vert(i, j, sudoku)
                    if len(sudoku[i, j]) == 1:
                        sudoku[i, j] = sudoku[i, j][0]
        # Testing columns.
        for i in range(9):
            sudoku = test_column(i, sudoku)
        # Testing rows.
        for j in range(9):
            sudoku = test_row(j, sudoku)
        # Test 3x3 squares.
        for x in range(3):
            for y in range(3):
                sudoku = test_3x3(x, y, sudoku)
        output(sudoku)
    return sudoku


hardest = deserialize_sudoku("800000000,003600000,070090200" +
                             "050007000,000045700,000100030" +
                             "001000068,008500010,090000400")
