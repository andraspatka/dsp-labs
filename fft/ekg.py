import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    ekg = np.loadtxt('ekg.csv', delimiter=",")
    t = ekg[0]
    ekg_val = ekg[1]
    N = len(t)

    plt.subplot(211)
    plt.plot(t, ekg_val)

    sp = np.fft.fft(ekg_val)
    freq = np.fft.fftfreq(N, t[1] - t[0])

    plt.subplot(212)
    plt.plot(freq, sp.real ** 2 + sp.imag ** 2)
    plt.show()