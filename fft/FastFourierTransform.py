import numpy as np
import matplotlib.pyplot as plt
import time
import math


def fft_own(xt):
    """A vectorized, non-recursive version of the Cooley-Tukey FFT"""
    x = np.asarray(xt, dtype=float)
    N = x.shape[0]

    if np.log2(N) % 1 > 0:
        raise ValueError("size of x must be a power of 2")

    # N_min here is equivalent to the stopping condition above,
    # and should be a power of 2
    N_min = min(N, 32)

    # Perform an O[N^2] DFT on all length-N_min sub-problems at once
    n = np.arange(N_min)
    k = n[:, None]
    M = np.exp(-2j * np.pi * n * k / N_min)
    X = np.dot(M, x.reshape((N_min, -1)))

    # build-up each level of the recursive calculation all at once
    while X.shape[0] < N:
        X_even = X[:, :int(X.shape[1] / 2)]
        X_odd = X[:, int(X.shape[1] / 2):]
        factor = np.exp(-1j * np.pi * np.arange(X.shape[0])
                        / X.shape[0])[:, None]
        X = np.vstack([X_even + factor * X_odd,
                       X_even - factor * X_odd])

    return X.ravel()


def brev(inDat):
    N = len(inDat)
    outDat = []
    for k in range(N):
        revN = int('{:0{width}b}'.format(k, width=int(np.ceil(np.log2(N))))[::-1], 2)
        outDat.append(inDat[revN])
    return outDat



if __name__ == "__main__":
    fig, axes = plt.subplots(ncols=1, nrows=2)
    ax1, ax2 = axes.ravel()

    # generate an input signal
    Num = 1024
    fs = 1000
    t = np.linspace(0, Num / fs, Num)
    x_t = np.sin(2 * np.pi * 1 * t) + 0.5 * np.sin(2 * np.pi * 5 * t) + 0.2 * np.sin(2 * np.pi * 10 * t)

    # Generate the FFT twiddle factors

    # Compute the FFT with time measurement
    start_time = time.time()
    X_f = fft_own(x_t)
    stop_time = time.time()

    f = np.linspace(0, fs / 2, int(Num / 2))
    # Magnitude
    A_f = np.zeros(Num, dtype=float)
    for k in range(Num):
        A_f[k] = np.sqrt(np.power(X_f[k].imag, 2) + np.power(X_f[k].real, 2))

    elapsed_time = stop_time - start_time
    print("The time of execution of our DFT is: %.5f s." % elapsed_time)

    # plot input signal
    ax1.plot(t, x_t)
    ax1.margins(0)
    ax1.grid()
    # plot output signal
    ax2.plot(f, A_f[0:int(Num / 2)])
    plt.xscale("log")
    ax2.margins(0)
    ax2.grid()
    plt.show()


