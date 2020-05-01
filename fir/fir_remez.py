from numpy import cos, sin, pi, absolute, arange, loadtxt, linspace
from scipy.signal import kaiserord, lfilter, firwin, freqz, remez
from pylab import figure, clf, plot, subplot, xlabel, ylabel, xlim, ylim, title, grid, axes, show

if __name__ == "__main__":
    x = loadtxt('noisy_ecg.csv', delimiter=",")
    len_ekg = len(x)
    t = linspace(0, len_ekg, len_ekg)

    sample_rate = 1000
    cutoff_hz = 250
    stop_hz = [40, 60]
    stop_width_hz = 2

    # ------------------------------------------------
    # Create a FIR filter and apply it to x.
    # ------------------------------------------------

    # The Nyquist rate of the signal.
    nyq_rate = sample_rate / 2.0

    num_taps = 750

    # Lowpass FIR with remez algo
    edges = [0, cutoff_hz, cutoff_hz + 10, 0.5 * sample_rate]
    taps = remez(num_taps, edges, [1, 0], Hz=sample_rate)

    # Bandstop FIR with remez algo
    edges = [0, stop_hz[0] - stop_width_hz, stop_hz[0], stop_hz[1], stop_hz[1] + stop_width_hz, 0.5 * sample_rate]
    taps2 = remez(num_taps, edges, [1, 0, 1], Hz=sample_rate)

    # Use lfilter to filter x with the FIR filter.
    filtered_x = lfilter(taps, 1.0, x)
    filtered_x = lfilter(taps2, 1.0, filtered_x)

    # ------------------------------------------------
    # Plot the FIR filter coefficients.
    # ------------------------------------------------

    figure(1)
    subplot(211)
    plot(taps, 'bo-', linewidth=2)
    title('Filter Coefficients - low pass (%d taps)' % num_taps)
    grid(True)

    subplot(212)
    plot(taps2, 'bo-', linewidth=2)
    title('Filter Coefficients - band stop (%d taps)' % num_taps)
    grid(True)

    # ------------------------------------------------
    # Plot the magnitude response of the filter.
    # ------------------------------------------------

    figure(2)
    clf()
    w, h = freqz(taps, worN=8000)
    plot((w / pi) * nyq_rate, absolute(h), linewidth=2)
    xlabel('Frequency (Hz)')
    ylabel('Gain')
    title('Frequency Response')
    ylim(-0.05, 1.05)
    grid(True)

    # Upper inset plot.
    ax1 = axes([0.42, 0.6, .45, .25])
    plot((w / pi) * nyq_rate, absolute(h), linewidth=2)
    xlim(0, 250)
    ylim(0.98, 1.05)
    grid(True)

    # Lower inset plot
    ax2 = axes([0.42, 0.25, .45, .25])
    plot((w / pi) * nyq_rate, absolute(h), linewidth=2)
    xlim(250.0, 300.0)
    ylim(0.0, 0.15)
    grid(True)

    # ------------------------------------------------
    # Plot the original and filtered signals.
    # ------------------------------------------------

    # The phase delay of the filtered signal.
    delay = 0.5 * (num_taps - 1) / sample_rate

    figure(4)
    # Plot the original signal.
    plot(t, x)
    # Plot the filtered signal, shifted to compensate for the phase delay.
    plot(t - delay, filtered_x, 'r-')
    # Plot just the "good" part of the filtered signal.  The first N-1
    # samples are "corrupted" by the initial conditions.
    plot(t[num_taps - 1:] - delay, filtered_x[num_taps - 1:], 'g', linewidth=4)

    xlabel('t')
    grid(True)

    show()
