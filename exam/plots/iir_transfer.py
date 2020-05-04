import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

fs = 20000
f = np.linspace(0, fs, fs)

b, a = signal.iirfilter(3, [1/2000], btype="lowpass", analog=False, output='ba', ftype="butter")

sys = signal.TransferFunction(a,b, dt=1/fs)

w, mag, phase = sys.bode()

plt.figure()
plt.plot(w, mag)    # Bode magnitude plot
plt.show()