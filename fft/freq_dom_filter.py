import numpy as np
import matplotlib.pyplot as plt
import scipy
import wavio


# def blueNoise(t, fs, fc, bd=32):
#    M = len(t)
#    x = np.random.uniform(-2 ** bd, 2 ** bd - 1, M)
#    X = np.fft.fft(x)
#    hp = fc / fs * M
#    Y = [X[i] if hp < i < M - hp else 0 for i in range(M)]
#    np.real(np.fft.ifft(Y))


def lp_filter(x, fs, fc, M=None, plot=False):
    if M is None:
        M = x.size
    Xf = scipy.fft.fft(x, n=M)
    Af = abs(Xf)

    # Convert cutoff frequencies into points on spectrum
    lp = fc / fs * M
    Y = [0 if lp < i < M - lp else Xf[i] for i in range(M)]

    y = scipy.fft.ifft(Y, n=M)

    if plot:

        plt.figure()
        plt.subplot(211)
        plt.plot(x)
        plt.plot(y)
        plt.grid(which='both')
        plt.minorticks_on()
        plt.subplot(212)
        plt.stem(Af[:len(Af)//2]*2.0/len(Af))
        plt.axis([0, fs / 2, None, None])
        plt.axvspan(0, lp, facecolor='g', alpha=0.5)
        plt.grid(which='both')
        plt.minorticks_on()
        plt.show()

    return y


def hp_filter(x, fs, fc, M=None, plot=False):
    if M is None:
        M = x.size
    Xf = scipy.fft.fft(x, n=M)
    Af = abs(Xf)

    # Convert cutoff frequencies into points on spectrum
    hp = fc / fs * M
    Y = [Xf[i] if hp < i < M - hp else 0 for i in range(M)]

    y = scipy.fft.ifft(Y, n=M)

    if plot:

        plt.figure()
        plt.subplot(211)
        plt.plot(x)
        plt.plot(y)
        plt.grid(which='both')
        plt.minorticks_on()
        plt.subplot(212)
        plt.stem(Af[:len(Af)//2]*2.0/len(Af))
        plt.axis([0, fs / 2, None, None])
        plt.axvspan(hp, fs/2, facecolor='g', alpha=0.5)
        plt.grid(which='both')
        plt.minorticks_on()
        plt.show()

    return y


def bp_filter(x, fs, fl, fh, M=None, plot=False):
    if M is None:
        M = x.size
    Xf = scipy.fft.fft(x, n=M)
    Af = abs(Xf)

    # Convert cutoff frequencies into points on spectrum
    hp = fh / fs * M
    lp = fl / fs * M
    Y = [Xf[i] if ((lp <= i <= hp) or (M-hp <= i <= M-lp) ) else 0 for i in range(M)]

    y = scipy.fft.ifft(Y, n=M)

    if plot:

        plt.figure()
        plt.subplot(211)
        plt.plot(x)
        plt.plot(y)
        plt.grid(which='both')
        plt.minorticks_on()
        plt.subplot(212)
        plt.stem(Af[:len(Af)//2]*2.0/len(Af))
        plt.axis([0, fs / 2, None, None])
        plt.axvspan(lp, hp, facecolor='g', alpha=0.5)
        plt.grid(which='both')
        plt.minorticks_on()
        plt.show()

    return y


def bs_filter(x, fs, fl, fh, M=None, plot=False):
    if M is None:
        M = x.size
    Xf = scipy.fft.fft(x, n=M)
    Af = abs(Xf)

    # Convert cutoff frequencies into points on spectrum
    hp = fh / fs * M
    lp = fl / fs * M
    Y = [0 if ((lp <= i <= hp) or (M-hp <= i <= M-lp) ) else Xf[i] for i in range(M)]

    y = scipy.fft.ifft(Y, n=M)

    if plot:

        plt.figure()
        plt.subplot(211)
        plt.plot(x)
        plt.plot(y)
        plt.grid(which='both')
        plt.minorticks_on()
        plt.subplot(212)
        plt.stem(Af[:len(Af)//2]*2.0/len(Af))
        plt.axis([0, fs / 2, None, None])
        plt.axvspan(0, lp, facecolor='g', alpha=0.5)
        plt.axvspan(hp, fs / 2, facecolor='g', alpha=0.5)
        plt.grid(which='both')
        plt.minorticks_on()
        plt.show()

    return y


if __name__ == "__main__":
    fs = 1000
    t = np.arange(0, 1, 1 / fs)
    Sines = [np.sin(2*np.pi*t*n)*(1-(n/500.0)) for n in [225.0, 187.5, 125.0, 62.5, 30.0, 7.5, 6.25]]
    x = np.sum(Sines, axis=0)

    #lp_filter(x, fs, 10.0, plot=True)
    #hp_filter(x, fs, 200.0, plot=True)
    #bp_filter(x, fs, 45.0, 80.0, plot=True)
    y1 = bs_filter(x, fs, 45.0, 200.0, plot=True)

    plt.figure()
    plt.magnitude_spectrum(y1, Fs=fs)
    plt.show()
