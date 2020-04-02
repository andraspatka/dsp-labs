import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import dct, idct


def cosSignal(freq=440, amp=1.0, time=0):
    return amp*np.cos(2*np.pi*freq*time)


def synthesyze1(amps, freqs, t):
   sums = []
   for ti in t:
       components = [cosSignal(freq, amp, ti) for freq, amp in zip(freqs, amps)]
       sum = 0.0
       for c in components:
           sum += c
       sums.append(sum)
   return sums


def synthesyze2(amps, freqs, t):
    args = np.outer(t, freqs)
    M = np.cos(2*np.pi*args)
    x = np.dot(M, amps)
    return x


def analyze1(y, fs, ts):
    args = np.outer(ts, fs)
    M = np.cos(2 * np.pi * args)
    amps = np.linalg.solve(M, y)
    return amps


def analyze2(y, fs, ts):
   pass


def dct_own(ys):
   N = len(ys)
   hs = dct(ys, type=2)
   fs = (0.5+np.arange(N)) / 2
   return hs, fs


def idct_own(hs):
   n = len(hs)
   ys = idct(hs, type=2) / 2 / n
   return ys

def main():
    amps = np.array([0.6, 0.25, 0.1, 0.05])
    freqs = [100, 200, 300, 400]
    sampling = 11025

    t, T = np.linspace(0, 1, sampling, retstep=True)

    y1 = synthesyze1(amps, freqs, t)
    y2 = synthesyze2(amps, freqs, t)

    plt.figure()
    plt.subplot(211)
    plt.plot(t, y1)
    plt.plot(t, y2)
    plt.subplot(212)
    X = np.fft.fft(y1)
    fs = 1 / T
    ReX = np.real(X)
    ReX = ReX[:int(len(ReX) / 2.0)]
    f = np.linspace(0, fs / 2, len(ReX))
    plt.plot(f, ReX)
    # plt.show()

    n = len(freqs)
    amps2 = analyze1(y2[:n], freqs, t[:n])
    print(amps2)

    N = 4.0
    time_unit = 0.001
    ts = np.arange(N) / N * time_unit
    max_freq = N / time_unit / 2
    fs = np.arange(N) / N * max_freq
    args = np.outer(ts, fs)
    M = np.cos(2 * np.pi * args)
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
    print(M)
    Mt = np.transpose(M)
    I = Mt.dot(M)
    print(I)

    # DCT IV

    ts = (0.5 + np.arange(N)) / N
    fs = (0.5 + np.arange(N)) / 2
    args = np.outer(ts, fs)
    M = np.cos(2 * np.pi * args)
    Mt = np.transpose(M)
    I = Mt.dot(M)
    print(I)

    h, f = dct_own(y1)
    print(h)
    plt.figure()
    plt.plot(f, h)

    plt.show()

    # from scipy.signal import find_peaks
    # peaks, _ = find_peaks(hs, height=10)


if __name__ == '__main__':
    main()

