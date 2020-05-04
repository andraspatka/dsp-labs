from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

fs = 20000
fc = 2000
a = [-1594.43, 1051.06, 0]
b = [1, -1.78, 0.53, -0.28]
s1 = signal.TransferFunction(a, b, dt=1/fs)
print(s1.poles)
sos_own = signal.tf2sos(a, b)
sos = signal.iirfilter(3, [fc], btype='lowpass', analog=False, ftype='butter', fs=fs, output='sos')
w, h = signal.sosfreqz(sos, fs=fs)
w_own, h_own = signal.sosfreqz(sos_own, fs=fs)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.semilogx(w, 20 * np.log10(abs(h)), label='Scipy')
ax.semilogx(w_own, 20 * np.log10(abs(h_own)), label='Saját')
ax.set_title('IIR - harmadfokú butterworth-ből')
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Amplitude [dB]')
ax.axis((10, 20000, -100, 250))
ax.grid(which='both', axis='both')
ax.legend()

plt.figure(2)

t = np.linspace(0, 2*np.pi, 401)
plt.plot(np.cos(t), np.sin(t), 'k--')  # unit circle
plt.plot(s1.poles.real, s1.poles.imag, 'bx', label='Pólusok')
plt.grid()
plt.axis('image')
plt.axis([-1.1, 1.7, -1.1, 1.1])
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, numpoints=1)
plt.show()