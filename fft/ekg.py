import numpy as np
import matplotlib.pyplot as plt
import time
from FastFourierTransform import fft_own

if __name__ == "__main__":
    ekg = np.loadtxt('ekg.csv', delimiter=",")
    dataLen = len(ekg[0])
    # fft_own requires pow of 2 number of samples
    N = 2 ** (int(np.log2(len(ekg[0]))) + 1)
    pad_len = N - dataLen
    t = np.append(ekg[0], np.zeros(pad_len))
    ekg_val = np.append(ekg[1], np.zeros(pad_len))

    # Plot the signal
    plt.subplot(311)
    plt.plot(t, ekg_val)

    fs = 1000
    start_time = time.time()
    sp = np.fft.fft(ekg_val)
    stop_time = time.time()
    elapsed_numpy = stop_time - start_time
    sp = sp[0:int(N/2)]
    f = np.linspace(0, fs / 2, int(N / 2))

    # Compute the FFT with time measurement
    start_time = time.time()
    X_f = fft_own(ekg_val)
    stop_time = time.time()

    # Magnitude
    A_f = np.sqrt(X_f.imag ** 2 + X_f.real ** 2)[0:int(N/2)]
    sp = np.sqrt(sp.imag ** 2 + sp.real ** 2)[0:int(N/2)]

    elapsed_time = stop_time - start_time
    print("The time of execution of our DFT (own) is: %.5f s." % elapsed_time)
    print("The time of execution of our DFT (np) is: %.5f s." % elapsed_numpy)

    plt.subplot(312)
    plt.plot(f, sp)

    plt.subplot(313)
    plt.plot(f, A_f)

    plt.show()