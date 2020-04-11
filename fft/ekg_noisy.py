import numpy as np
import matplotlib.pyplot as plt
import scipy

def is_band_pass(n, N, sc, cut_band_width):
    return n < sc - cut_band_width or (n > sc + cut_band_width and n < N - sc - cut_band_width) or n > N - sc + cut_band_width

def is_low_pass(n, N, sc):
    return n < sc or n > N - sc

if __name__ == "__main__":
    ekg = np.loadtxt('noisy_ecg.csv', delimiter=",")
    N = len(ekg)
    ekg_val = ekg
    t = np.linspace(0, N, N)

    fs = 1000
    fc = 50
    fc_low_pass = 250
    sp = scipy.fft.fft(ekg_val, n=N)
    f = np.linspace(0, fs, N)

    # Magnitude
    sp_org = sp
    sp = np.sqrt(sp.imag ** 2 + sp.real ** 2)
    sc = fc / fs * N
    sc_low_pass = fc_low_pass / fs * N
    cut_band_width = 10

    band_stop_plt = [1000 if is_band_pass(n, N, sc, cut_band_width) else 0 for n in range(N)]
    low_pass_plt = [1000 if is_low_pass(n, N, sc_low_pass) else 0 for n in range(N)]
    # bandstop filter
    xf = [sp_org[n] if is_band_pass(n, N, sc, cut_band_width) else 0 + 0j for n in range(N)]
    # low pass filter
    xf = [xf[n] if is_low_pass(n, N, sc_low_pass) else 0 + 0j for n in range(N)]

    xf = scipy.fft.ifft(xf, n=N)

    part_plot = N
    # Plot the signal
    plt.subplot(311)
    plt.plot(t[0:part_plot], ekg_val[0:part_plot])

    # fft
    plt.subplot(312)
    plt.plot(f, sp)
    # plot the filters
    plt.plot(f, band_stop_plt)
    plt.plot(f, low_pass_plt)

    # plot the result
    plt.subplot(313)
    plt.plot(xf[0:part_plot])

    plt.show()
