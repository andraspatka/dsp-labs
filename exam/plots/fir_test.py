import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

if __name__ == '__main__':
    fs = 5000
    Ts = 1/fs
    Ns = 1024

    # Generate the signal
    f1 = 500
    f2 = 2000
    t = np.arange(0, 1, Ts)
    x1 = np.sin(2 * np.pi * f1 * t)
    x2 = np.sin(2 * np.pi * f2 * t)
    x = x1 + x2

    x = x[:Ns]
    t = t[:Ns]

    # Plot the signal and the magnitude spectrum
    plt.figure(1)
    plt.subplot(211)
    plt.plot(t, x)
    plt.subplot(212)
    X = np.fft.fft(x)
    X = X[:int(len(X)/2)]
    f = np.linspace(0, fs/2, len(X))
    A = np.sqrt(np.imag(X)**2 + np.real(X)**2)
    A = A/len(A)
    plt.plot(f, A)

    #Design a LP FIR filter
    fc = 1000
    wc = fc*np.pi/fs
    n = np.arange(0, Ns)
    h = np.sin(wc*(n - (Ns-1)/2))/(np.pi*(n - (Ns-1)/2))
    # print(h[int((Ns-1)/2)])
    # print(wc/np.pi)
    plt.figure(2)
    plt.plot(n, h)

    #Filter the signal with convolution
    y1 = np.convolve(x,h,mode='same')
    plt.figure(1)
    plt.subplot(211)
    plt.plot(t, y1)
    plt.subplot(212)
    Y = np.fft.fft(y1)
    Y = Y[:int(len(Y) / 2)]
    f = np.linspace(0, fs / 2, len(Y))
    Ay = np.sqrt(np.imag(Y) ** 2 + np.real(Y) ** 2)
    Ay = Ay / len(Ay)
    plt.plot(f, Ay)

    # Design a window for the filter - Triangle
    tri_win = 1 - np.abs((2*n-Ns+1)/(Ns-1))
    h_win = np.multiply(h, tri_win)
    plt.figure(2)
    #plt.plot(n, tri_win)
    plt.plot(n, h_win)

    # Filter the signal with convolution
    y2 = np.convolve(x, h_win, mode='same')
    plt.figure(1)
    plt.subplot(211)
    plt.plot(t, y2)
    plt.subplot(212)
    Y = np.fft.fft(y2)
    Y = Y[:int(len(Y) / 2)]
    f = np.linspace(0, fs / 2, len(Y))
    Ay = np.sqrt(np.imag(Y) ** 2 + np.real(Y) ** 2)
    Ay = Ay / len(Ay)
    plt.plot(f, Ay)

    # check the filter response
    w1, h1 = freqz(h, worN=8000)
    f = np.linspace(0,fs/2,8000)
    w2, h2 = freqz(h_win, worN=8000)
    plt.figure(3)
    plt.plot(f,np.abs(h1))
    plt.plot(f, np.abs(h2))



    plt.show()