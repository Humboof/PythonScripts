from scipy.optimize import fsolve, root
import numpy as np
from scipy.interpolate import griddata


def friction(eps, D, Re):
    term1 = 1/2.8257 * (eps/D)**1.1098 + 5.8506/(Re**0.8981)
    term2 = 5.0452/Re * np.log10(term1)
    term3 = -2.0 * np.log10(eps/3.7065/D - term2)
    return term3**-2


def flowerror(Q, rho, mu, eps, L, D):
    q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, qout1 = Q  # naming helps
    npipes = len(Q)-1  # the last Q unknown is not a pipe
    dp = np.zeros(npipes)
    for i in range(npipes):
        v = 4*Q[i]/np.pi/(D[i]**2)
        Re = rho*abs(v)*D[i]/mu
        f = friction(eps[i], D[i], Re)
        dp[i] = -f*L[i]*abs(v)*v*rho/(2*D[i])
    # next i
    p1, p2, p3, p4, p5, p6, p7, p8, p9, p10 = dp  # naming helps!

    errors = [0.300-q1-q2,
              q1-q5-q3,
              q5-q7-qout1,
              q3-q6+q8-0.100,
              q6+q7-q10,
              q2-q4,
              q4-q8-q9,
              q9+q10-0.150,
              p1+p3-p8-p4-p2,
              p5+p7-p6-p3,
              p6+p10-p9+p8]

    return errors


def main():

    rho = 800
    mu = 0.0006

    L = np.array([300,250,125,300,350,350,125,125,350,125])
    D = np.array([.3,.25,.2,.2,.2,.2,.2,.15,.2,.15])
    EoverD = np.array([87,104,130,130,130,130,130,173,130,173])*0.00001
    eps = EoverD * D  # to get an eps array

    guess = np.ones(11) * 10  # could scale the guesses
    Qvals = fsolve(flowerror,guess,args=(rho,mu,eps,L,D))
    Qvals = fsolve(flowerror,Qvals,args=(rho,mu,eps,L,D))
    # Qvals = fsolve(flowerror,Qvals,args=(rho,mu,eps,L,D))

    print('The flow in section 1 is {:.1f} liters/s'.format(1000 * Qvals[0]))
    print('The flow in section 2 is {:.1f} liters/s'.format(1000 * Qvals[1]))
    print('The flow in section 3 is {:.1f} liters/s'.format(1000 * Qvals[2]))
    print('The flow in section 4 is {:.1f} liters/s'.format(1000 * Qvals[3]))
    print('The flow in section 5 is {:.1f} liters/s'.format(1000 * Qvals[4]))
    print('The flow in section 6 is {:.1f} liters/s'.format(1000 * Qvals[5]))
    print('The flow in section 7 is {:.1f} liters/s'.format(1000 * Qvals[6]))
    print('The flow in section 8 is {:.1f} liters/s'.format(1000 * Qvals[7]))
    print('The flow in section 9 is {:.1f} liters/s'.format(1000 * Qvals[8]))
    print('The flow in section 10 is {:.1f} liters/s'.format(1000 * Qvals[9]))
    print('The flow out between 5 and 7 is {:.1f} liters/s'.format(1000 * Qvals[10]))

    print(flowerror(Qvals, rho, mu, eps, L, D))


main()
