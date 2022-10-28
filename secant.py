from math import cos, sin, fabs


def Secant(func, x0, x1, maxiter=15, xtol=0.0001):
    # use the secant method to estimate the root of func()
    for i in range(maxiter):
        # use the secant equation in a loop
        xnew = x1 - func(x1) * (x1 - x0) / (func(x1) - func(x0))
        if fabs(xnew - x1) < xtol:  # are we converged?
            return xnew  # yes, so exit early
        else:
            x0 = x1
            x1 = xnew  # update and do it again
        return xnew


def main():
    def f1(x):
        return x - 3 * sin(x)

    def f2(x):
        return cos(2 * x) * x ** 3

    root = Secant(f1, 1, 2, 5, 1e-4)
    print('the root is: {:.6f} after 5 iterations'.format(root))

    root = Secant(f2, 1, 2, 15, 1e-8)
    print('the root is: {:.6f} after 15 iterations'.format(root))

    root = Secant(f2, 1, 2, 3, 1e-8)
    print('the root is: {:.6f} after 3 iterations'.format(root))


if __name__ == '__main__':
    main()
