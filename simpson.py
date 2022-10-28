from math import sin, cos, fabs


def Simpson(func, a, b, npoints = 35):
    # use the Simpson 1/3 rule to estimate the integral value

    if npoints % 2 == 0:  # npoints is even, but must be odd
        npoints += 1  # make it odd!
    # simpson has a 1 4 2 4 2 4 2 ..... 2 4 1
    h = (b - a) / (npoints - 1)  # npoints - 1 is the number of intervals
    sum = func(a) + func(b)  # the first and last terms
    for i in range(1, npoints, 2):  # the odd terms
        sum += 4 * func(a + i * h)  # are multiplied by 4
    for i in range(2, npoints -1, 2):  # the even terms
        sum += 2 * func(a + i * h)  # are multiplied by 2
    return sum * h / 3


def main():

    def f1(x):
        return x - 3 * sin(x)

    def f2(x):
        return cos(2*x)*x**3

    integral = Simpson(f1, 1, 3, 10)
    print('the integral of function 1 is: {:.7f} '.format(integral))

    integral = Simpson(f2, 2, 3, 23)
    print('the integral of function 2 is: {:.2f} '.format(integral))

    integral = Simpson(f2, 2, 3)
    print('the integral of function 2 is: {:.2f} '.format(integral))


if __name__ == '__main__':
    main()
