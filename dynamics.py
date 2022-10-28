from scipy.optimize import fsolve
import numpy as np
import matplotlib.pyplot as plt


def dynamics(vals, theta):
    va, t = vals  # extract the current guesses
    error1 = t - 80/(va * np.cos(theta))
    error2 = 4.905*t**2 - va*np.sin(theta)*t - 64
    return (error1, error2)


def solver(theta):
    guesses = [1,1]  # 2 unknowns therefore 2 guesses
    va, t = fsolve(dynamics, guesses, args = (theta,))
    return va


def main():
    # thvals = np.pi/180 * np.array([15,20,25,30,35,40,45,50,55,60])
    thvals = np.pi/180 * np.linspace(15, 60, 10)
    va = np.zeros_like(thvals)  # right size - wrong values

    for i in range(len(thvals)):  # for all angles
        va[i] = solver(thvals[i])  # solve for the required speed

    plt.plot(thvals*180/np.pi, va)
    plt.title('Required Launch Speed vs Launch Angle')
    plt.xlabel('Launch Angle')
    plt.ylabel('Required Launch Speed')
    plt.show()


main()
