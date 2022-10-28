from copy import deepcopy
import numpy as np


def PartialPivot(matrix, pivotrow):
    # look below the given pivot row for a better pivot term
    nrows = len(matrix)
    ncols = len(matrix[0])
    betterrow = pivotrow  # assume pivotrow is the best row
    pivotval = abs(matrix[pivotrow][pivotrow])  # value of the pivot term
    for newrow in range(pivotrow + 1, nrows):  # search for a better row
        newval = abs(matrix[newrow][pivotrow])
        if newval > pivotval:  # then there is a better term
            pivotval = newval  # this is better, but might not be the BEST
            betterrow = newrow
    # at this point, we know the BEST row
    if betterrow > pivotrow:  # if we found a better row
        # swap each term in the two rows
        # in most languages, a swap requires 3 lines
        for col in range(ncols):
            # do it the common way with 3 lines
            temp = matrix[pivotrow][col]
            matrix[pivotrow][col] = matrix[betterrow][col]
            matrix[betterrow][col] = temp
            # or do it in one line, using Python's unique syntax
            # matrix[pivotrow][col], matrix[betterrow][col] = matrix[betterrow][col], matrix[pivotrow][col]
    return matrix


def GaussElim(AaugIn):
    N = len(AaugIn)  # the number of equations
    Aaug = deepcopy(AaugIn)
    # the elimination
    for helperRow in range(N - 1):  # don't use the last row as a helperRow
        PartialPivot(Aaug, helperRow)
        helperRowTerm = Aaug[helperRow][helperRow]  # we sure hope it isn't ZERO
        for targetRow in range(helperRow + 1, N):  # loop to the last targetRow
            R = Aaug[targetRow][helperRow] / helperRowTerm
            Aaug[targetRow][helperRow] = 0
            for col in range(helperRow + 1, N+1):  # loop to the last col of Aaug
                Aaug[targetRow][col] -= Aaug[helperRow][col] * R
            # next col
        # next targetRow
    # next helperRow

    # back substitution
    x = [0.0]*len(Aaug)
    for row in range(N - 1, -1, -1):  # all rows of Aaug  ... backwards
        x[row] = Aaug[row][N]  # the RHS value for this row
        for col in range(row + 1, N):  # to the end of the Aaug matrix
            x[row] -= Aaug[row][col] * x[col]  # subtracting the appropriate value
        # next col
        x[row] = x[row] / Aaug[row][row]  # and divide by the diagonal term
    # next row

    return x


def printmatrix(matrix):
    for row in matrix:
        print(row)
    print()


def main():
    A = [[0,0,-4,4],[-6,4,8,9],[2,-4,6,8],[4,5,2,1]]
    b = [5, 10, 10, 0]
    Aaug = [[0,0,-4,4,5],[-6,4,8,9,10],[2,-4,6,8,10],[4,5,2,1,0]]

    print('Original')
    printmatrix(Aaug)

    print('Call GaussElim and numpy solver - print the answers and the matrix')
    print(GaussElim(Aaug))
    print(np.linalg.solve(A, b))
    printmatrix(Aaug)

    PartialPivot(Aaug,0)
    print('pivot on row 0 gives ')
    printmatrix(Aaug)

    PartialPivot(Aaug,1)
    print('pivot on row 1 gives ')
    printmatrix(Aaug)

    PartialPivot(Aaug,2)
    print('pivot on row 2 gives ')
    printmatrix(Aaug)

    PartialPivot(Aaug,3)
    print('pivot on row 3 gives ')
    printmatrix(Aaug)


main()
