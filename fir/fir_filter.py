import numpy as np
import matplotlib.pyplot as plt
import scipy

if __name__ == "__main__":
    ekg = np.loadtxt('noisy_ecg.csv', delimiter=",")
    N = len(ekg)
    ekg_val = ekg
    t = np.linspace(0, N, N)

    fs = 1000
    fc = 50
    fc_low_pass = 250

    # Plot the signal
    plt.subplot(211)
    plt.plot(t[0:N], ekg_val[0:N])

    # plot the result
    #plt.subplot(212)
    #plt.plot(xf[0:part_plot])

    plt.show()
