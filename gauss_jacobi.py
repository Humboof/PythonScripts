import numpy as np  # just for checking the answers using the numpy solver


def GaussJacobi(A, b, xguess, maxiter = 1):
    n = len(xguess)  # the size of the square coeff. matrix (the A-matrix)
    xnew = [0]*n  # storage for xnew ... we delay using the new answers
    for i in range(maxiter):  # perform the required number of iterations
        for row in range(n):  # loop over each equation
            sum = b[row]  # start with the right-hand side value
            for col in range(n):  # loop over every term in this equation
                if row != col:  # if this is not the diagonal term
                    sum = sum - A[row][col] * xguess[col]  # add the other terms
            xnew[row] = sum / A[row][row]  # then divide the sum by the diagonal
        # next row
        for i in range(n): xguess[i] = xnew[i]  # copy xguess to xnew

    # next i    # next iteration
    return xnew


def main():

    A1 = [[4, -1, -1],
          [-2, -3, 1],
          [-1, 1, 7]]

    b1 = [3, 9, -6]

    A2 = [[4, 3, 1, -1],
          [2, -5, 0, -2],
          [-3, 3, -6, 1],
          [0, 1, 4, 8]]

    b2 = [2, -3, 5, -2]

    answer = GaussJacobi(A1, b1, [0, 0, 0], maxiter=22)
    print(answer)
    answer = np.linalg.solve(A1, b1)
    print(answer)

    answer = GaussJacobi(A2, b2, [1, 1, 1, 1], maxiter=22)
    print(answer)
    answer = np.linalg.solve(A2, b2)
    print(answer)


if __name__ == '__main__':
    main()
