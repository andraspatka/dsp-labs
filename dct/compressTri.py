from scipy import signal
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import numpy as np

from scipy.fftpack import dct, idct


if __name__ == "__main__":
    t = np.linspace(0, 1, 500)
    tri = signal.sawtooth(2 * np.pi * 5 * t, 0.5)

    hs = dct(tri, type=2)
    fs = (0.5 + np.arange(len(hs))) / 2

    compressed_len = 40

    # inverse dct, lossy compression
    hs_compressed = hs[0:compressed_len]
    tri_compressed = idct(hs_compressed, type=2)
    # scale it back to -1, 1
    tri_compressed = tri_compressed / 500
    t_compressed = np.linspace(0, 1, len(tri_compressed))

    peaks, _ = find_peaks(-hs, height=10)

    plt.figure()
    plt.subplot(411)
    plt.plot(t, tri)
    plt.subplot(412)
    plt.plot(fs, hs)
    plt.plot(peaks, hs[peaks])
    plt.subplot(413)
    plt.plot(fs[:compressed_len], hs[:compressed_len])
    plt.subplot(414)
    plt.plot(t_compressed, tri_compressed)
    plt.show()
