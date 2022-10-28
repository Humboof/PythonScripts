import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

# the function times the sine terms
# important - func is sent as an ARG    ... you may have to think hard on this


def fb(x, func, n, L):
    return func(x) * np.sin(n * np.pi * x / L)


def FourierCoeffs(func, L, nterms):
    # calculate the coefficients of a Fourier Series
    # for a periodic function over the range -L to L

    # the function times the cosine terms
    # no args needed for this one .... func() is inherited
    def fa(x):  # calculate the a's
        return func(x) * np.cos(n * np.pi * x / L)

    # create the a and b arrays
    a = np.zeros(nterms)  # right size, wrong values
    b = np.zeros(nterms)

    integral, error = quad(func, -L, L)  # quad returns 2 values
    a[0] = 1 / (2 * L) * integral  # the a0 term

    for n in range(1, nterms):  # get the Fourier Coefficients
        (Ia,error)=quad(fa, -L, L)  # integrate to get the a's
        # (Ia,error)=quad(lambda x: func(x) * np.cos(n * np.pi * x / L), -L, L)  # integrate to get the a's
        a[n] = 1 / L * Ia

        # notice two things - FUNC is sent to fb as an ARG
        #  and the [0] at the end of QUAD - to extract the value only
        b[n] = 1 / L * quad(fb, -L, L, args=(func,n,L))[0]  # [0] means take only the first value
    # next n

    return a, b


def evalFourier(a, b, L, x0, x1, npoints):

    # use the fourier coefficients to generate data for plotting

    X = np.linspace(x0, x1, npoints)  # generate X-Y data, right size and values
    Y = np.zeros(len(X))  # right size, wrong values
    for i in range(npoints):  # and outer loop over all x values
        sum = a[0]
        for j in range(1, len(a)):  # an inner loop over all a and b terms
            sum = sum + a[j] * np.cos(j * np.pi * X[i] / L)
            sum = sum + b[j] * np.sin(j * np.pi * X[i] / L)
        # next j
        Y[i] = sum # transfer the sum to the Y array
    # next i  # go to the next x value
    return X, Y  # return the X and Y arrays ... suitable for plotting


def PlotFourier(func, L, nterms, xmin, xmax, npoints=5000):
    a, b = FourierCoeffs(func, L, nterms)
    # plot the Fourier Series given by an and b
    X, Y = evalFourier(a, b, L, xmin, xmax, npoints)
    plt.plot(X, Y)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Fourier Series")
    plt.show()


def main():
    def Sharkfin(x):
        if x < 0:
            return (x + 1) ** 3
        else:
            return 1 - x ** 3

    def Squarewave(x):
        if x < 0:
            return 1
        else:
            return -1

    L = 1
    a, b = FourierCoeffs(Sharkfin, L, 50)
    print(a, "\n", b, "\n")
    PlotFourier(Sharkfin, L, 50, -3 * L, 3 * L)

    L = 0.75
    a, b = FourierCoeffs(Squarewave, L, 50)
    print(a, "\n", b, "\n")
    PlotFourier(Squarewave, L, 50, -3 * L, 3 * L)

    L = np.pi
    a, b = FourierCoeffs(lambda x: -x, L, 10)
    print(a, "\n", b, "\n")
    PlotFourier(lambda x: -x, L, 10, -4 * L, 4 * L, npoints=10000)


main()

