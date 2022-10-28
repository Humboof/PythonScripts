import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def toPolar(r):
    length = np.sqrt(r[0]**2 + r[1]**2)
    angle = np.arctan2(r[1],r[0])
    return length, angle


def couplerPoints(l, th):

    def loops(guesses):
        th3, th4 = guesses
        error1 = l[1]*np.cos(th[1]) + l[2]*np.cos(th2[i]) \
                 + l[3] * np.cos(th3) + l[4] * np.cos(th4)
        error2 = l[1] * np.sin(th[1]) + l[2] * np.sin(th2[i]) + \
                 + l[3] * np.sin(th3) + l[4] * np.sin(th4)
        return [error1, error2]

    th2 = np.linspace(th[2], th[2]+ 2 * np.pi, 37)
    th3 = np.zeros_like(th2)
    th4 = np.zeros_like(th2)
    pathx = np.zeros_like(th2)
    pathy = np.zeros_like(th2)
    alpha = th[5] - th[3]

    # initialize the ZERO elements of the arrays to the starting values
    th3[0] = th[3]
    th4[0] = th[4]
    pathx[0] = l[2]*np.cos(th[2]) + l[5] * np.cos(th[3] + alpha)
    pathy[0] = l[2]*np.sin(th[2]) + l[5] * np.sin(th[3] + alpha)

    # loop over all values of th2 and use fsolve() to get corresponding
    # values of th3, th4, pathx and pathy
    for i in range(1,37):
        guesses = np.array([th3[i-1], th4[i-1]])
        th3[i], th4[i] = fsolve(loops, guesses)
        loops([th3[i], th4[i]])
        pathx[i] = l[2]*np.cos(th2[i]) + l[5] * np.cos(th3[i] + alpha)
        pathy[i] = l[2]*np.sin(th2[i]) + l[5] * np.sin(th3[i] + alpha)

    return th2, th3, th4, pathx, pathy


def main():
    # the coordinates for the initial position of the machine
    a0 = np.array([0, 0])
    a = np.array([0, 2])
    p = np.array([1, 1])
    b = np.array([2, 3])
    b0 = np.array([1, 0])

    # x-y coordinates to draw the machine in the initial position
    # points in order:  a0, a, p, b, a, b, b0
    machinex = [a0[0],a[0],p[0],b[0],a[0],b[0],b0[0]]
    machiney = [a0[1],a[1],p[1],b[1],a[1],b[1],b0[1]]

    # the vectors in the initial position of the machine
    r2 = a - a0
    r3 = b - a
    r4 = b0 - b
    r1 = a0 - b0
    r5 = p - a

    # convert the 5 vectors to polar form (length and angle)
    # notice I am wasting position 0 in the vector arrays
    l = np.zeros(6)
    th = np.zeros(6)
    l[2], th[2] = toPolar(r2)
    l[3], th[3] = toPolar(r3)
    l[4], th[4] = toPolar(r4)
    l[1], th[1] = toPolar(r1)
    l[5], th[5] = toPolar(r5)

    alpha = th[5] - th[3]

    # get the motion variables th2, th3, etc for each position of the machine
    th3, th3, th4, pathx, pathy = couplerPoints(l, th)

    # This plot required for regular full credit
    plt.plot(machinex, machiney)
    plt.plot(pathx, pathy, "ro")
    plt.title('Fourbar Path Analysis')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(['Coupler Path', 'Machine'])
    plt.show()


main()


