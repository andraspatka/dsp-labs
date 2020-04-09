import numpy as np
import matplotlib.pyplot as plt
import time
import math


def iexp(n):
    return complex(math.cos(n), math.sin(n))


if __name__ == "__main__":
    # style.use('ggplot')
    fig, axes = plt.subplots(ncols=1, nrows=2)
    ax1, ax2 = axes.ravel()

    # generate an input signal
    Num = 1024
    fs = 1000
    t = np.linspace(0, Num/fs, Num)
    x_t = np.sin(2*np.pi*1*t) + 0.5*np.sin(2*np.pi*5*t) + 0.2*np.sin(2*np.pi*10*t)

    # Generate the twiddle factors for a 32p DFT
    N = 1024
    W = np.zeros([N, N], dtype=complex)
    for k in range(N):
        for i in range(N):
            W[k, i] = iexp(-2 * math.pi * i * k / N)

    # Compute the N point DFT with time measurement
    start_time = time.time()
    X_f = np.zeros(Num, dtype=complex)
    for k in range(N):
        temp_sum = complex(0)
        for i in range(N):
            temp_sum += x_t[i]*W[k, i]
        X_f[k] = temp_sum
    stop_time = time.time()
    # Compute the magnitude and frequency
    A_f = np.zeros(Num, dtype=float)
    for k in range(N):
        A_f[k] = np.sqrt(np.power(X_f[k].imag, 2) + np.power(X_f[k].real, 2))

    f = np.linspace(0, fs/2, int(Num/2))

    elapsed_time = stop_time - start_time
    print("The time of execution of our DFT is: %.2f s." % elapsed_time)

    # plot input signal
    ax1.plot(t, x_t)
    ax1.margins(0)
    ax1.grid()
    # plot output signal
    ax2.plot(f, A_f[0:int(Num/2)])
    plt.xscale("log")
    ax2.margins(0)
    ax2.grid()
    plt.show()
