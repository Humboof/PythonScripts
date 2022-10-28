import numpy as np
import matplotlib.pyplot as plt


def LeastSquares(x,y, power):

    # build the A matrix and sum arrays
    A = np.zeros((power + 1, power + 1))
    sumx = np.zeros(power * 2 + 1)  # sums are initialized to zero HERE AND THERE!
    sumxy = np.zeros(power + 1)

    # Build an array containing the sum of power of x
    for pow in range(power * 2 + 1):  # loop over the required powers
        for j in range(len(x)):  # sum over all points
            sumx[pow] += x[j] ** pow
        # next j
    # next power

    # build an array containing the sum of xy powers
    for pow in range(power + 1):  # loop over all required powers
        for j in range(len(x)):  # sum over all points
            sumxy[pow] += y[j] * x[j] ** pow
        # next j
    # next power

    # fill the A-matrix
    for row in range(power + 1):  # all rows of A
        for col in range(power + 1):  # all cols of A
            A[row][col] = sumx[row+col]
        # next col
    # next row

    a = np.linalg.solve(A, sumxy)  # solve for the a's
    return a


def poly(x, coeffs):
    n = len(coeffs)
    sum = coeffs[0]
    for i in range(1,n):
        sum += coeffs[i] * x**i
    # next i
    return sum


def PlotLeastSquares(x, y, power, showpoints = True, npoints = 500):
    a = LeastSquares(x, y, power)  # perform the least squares fit

    # calculate points for plotting
    minx = min(x); maxx = max(x)  # x values might not be in increasing order
    xvals = np.linspace(minx,maxx, npoints)  # xvalues for plotting
    yvals = np.zeros_like(xvals)  # preload with zeros to start a sum!!

    # loop and create the yvals
    for i in range(len(xvals)):
        yvals[i] = poly(xvals[i], a)
    # next i


    plt.plot(xvals, yvals)
    if showpoints: plt.plot(x,y,"ro")
    plt.title("Least Squares Curve Fitting")
    plt.show()


def main():
    x = [.05, .11, .15, .31, .46, .52, .7, .74, .82, .98, 1.17]
    y = [.956, 1.09, 1.332, .717, .771, .539, .378, .370, .306, .242, .104]

    a1 = LeastSquares(x, y, 1)  # solve the linear fit
    print(a1)
    PlotLeastSquares(x, y, 1)

    a3 = LeastSquares(x, y, 3)  # solve the cubic fit
    print("\n", a3)
    PlotLeastSquares(x, y, 3, showpoints=False)

    a = LeastSquares(x[0:5], y[0:5], 2)  # solve the cubic fit
    print("\n", a3)
    PlotLeastSquares(x[0:5], y[0:5], 2, showpoints=True)


if __name__ == '__main__':
    main()




