from scipy import signal
import matplotlib.pyplot as plt
import numpy as np


t = np.linspace(0, 2 * np.pi, 1000)

def f(t): return np.exp(- np.complex(0, 1) * t)
def c(t): return np.cos(t) + np.complex(0, 1) * np.sin(t)

plt.figure(1)
plt.subplot(211)
plt.plot(f(t).real, f(t).imag, "b")
plt.subplot(212)
plt.plot(c(t).real, c(t).imag, "b")
plt.show()


