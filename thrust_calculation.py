import numpy as np
import matplotlib.pyplot as plt
from simpson import Secant, Simpson


def STO(Thrust):  # Takeoff distance given Thrust

    def func(V):  # optional ... or use a lambda function
        return V/(A-B*V**2)

    # define parameters
    gc = 32.2; rho = 0.002377;
    CD = 0.0279; CLmax = 2.4;
    Weight = 56000; S = 1000;

    # the five equations
    Vstall = np.sqrt(Weight/(1/2*rho*S*CLmax))
    VTO = 1.2 * Vstall
    A = gc*Thrust/Weight
    B = gc/Weight*(1/2*rho*S*CD)
    # this final equation is an integral!
    # can use a lambda function, or define an actual function
    Dist = Simpson(lambda V: V/(A-B*V**2), 0, VTO, 101)
    Dist = Simpson(func, 0, VTO, 101)  # alternative
    return Dist


def ThrustNeededForTakeoff(distance):  # Thrust given Takeoff distance
    # this is a standard INVERSE form
    def func(Thrust):  # optional ... or use lambda
        return STO(Thrust) - distance

    T = Secant(func,1000,2000)  # use func or a lambda function
    T = Secant(lambda thrust: STO(thrust) - distance, 1000, 2000)
    return T


def main():
    D = STO(13000)
    print("Takeoff distance with 13000 pounds thrust is:  {:1f}".format(D))

    thrust = ThrustNeededForTakeoff(1500)
    print("Thrust required for a 1500 foot takeoff is {:2f}".format(thrust))

    thrust = ThrustNeededForTakeoff(1000)
    print("Thrust required for a 1000 foot takeoff is {:2f}".format(thrust))
    print(STO(thrust))

    th = np.linspace(5000, 30000, 50)
    dist = np.zeros_like(th)

    dist = STO(th)  # this works because of how STO was written

    # for i in range(len(th)):  #this works too!
    #   dist[i] = STO(th[i])

    plt.plot(th,dist)
    plt.xlabel("thrust")
    plt.ylabel("STO")
    plt.title("Takeoff Distance vs Thrust")
    plt.show()


main()
