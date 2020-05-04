import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

fs = 1000   # mintavételezési frekvencia (Hz)
fc = 400    # vágási frekvencia (Hz)
Ts = 1 / fs
Ns = 17     # FIR szűrő súlyfüggvényének nem nulla elemeinek száma

f1 = 10  # az első jel 100 Hz-es
f2 = 470 # a második jel 2 kHz-es
t = np.arange(0, 1, Ts)
x1 = np.sin(2 * np.pi * f1 * t)
x2 = np.sin(2 * np.pi * f2 * t)
x = x1 + x2

X = np.fft.fft(x)
X = X[:int(len(X)/2)]
f = np.linspace(0, fs/2, len(X))
A = np.sqrt(np.imag(X)**2 + np.real(X)**2)
A = A/len(A)


plt.figure(1)
plt.subplot(311)
plt.plot(t, x1, label="x1: 10Hz")
plt.plot(t, x2, label="x2: 470Hz")
plt.xlabel("t")
plt.ylabel("A")
plt.legend()
plt.subplot(312)
plt.plot(t, x, label="x1 + x2")
plt.xlabel("t")
plt.ylabel("A")
plt.legend()
plt.subplot(313)
plt.xlabel("f")
plt.ylabel("A")
plt.plot(f, A)

# Design a LP FIR filter
wc = 2 * np.pi * fc / fs
h = np.zeros(Ns)
n = np.arange(0, Ns)
nk = n[0:int(Ns/2)]
h[0:int(Ns/2)] = np.sin(wc * (nk - (Ns - 1) / 2)) / (np.pi * (nk - (Ns - 1) / 2))
h[int(Ns/2)] = 4 / 5
nk = n[int(Ns/2) + 1:Ns]
h[int(Ns/2) + 1:Ns] = np.sin(wc * (nk - (Ns - 1) / 2)) / (np.pi * (nk - (Ns - 1) / 2))

tri_win = 1 - np.abs((2*n-Ns+1)/(Ns-1))
h_win = np.multiply(h, tri_win)

plt.figure(2)
plt.subplot(211)
plt.stem(n, h, label="h[n]")
plt.plot(n, tri_win, label="Háromszög ablak")
plt.xlabel("n")
plt.ylabel("h[n]")
plt.legend()
plt.subplot(212)
plt.xlabel("n")
plt.ylabel("h[n]")
plt.stem(n, h_win)

plt.figure(3)

# Szűrés

plt.subplot(211)
plt.title("Ablakozás nélkül")
y1 = np.convolve(x, h, mode='same')
plt.plot(t, y1)
plt.xlabel("t")
plt.ylabel("A")
plt.subplot(212)
X = np.fft.fft(y1)
X = X[:int(len(X)/2)]
f = np.linspace(0, fs/2, len(X))
A = np.sqrt(np.imag(X)**2 + np.real(X)**2)
A = A/len(A)
plt.xlabel("f")
plt.ylabel("A")
plt.plot(f, A)

plt.figure(4)
plt.subplot(211)
plt.title("Ablakozással")
y2 = np.convolve(x, h_win, mode='same')
plt.plot(t, y1)
plt.xlabel("t")
plt.ylabel("A")
plt.subplot(212)
X = np.fft.fft(y2)
X = X[:int(len(X)/2)]
f = np.linspace(0, fs/2, len(X))
A = np.sqrt(np.imag(X)**2 + np.real(X)**2)
A = A/len(A)
plt.xlabel("f")
plt.ylabel("A")
plt.plot(f, A)



plt.show()