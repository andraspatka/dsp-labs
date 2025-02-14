from numpy import cos, sin, pi, absolute, arange, loadtxt, linspace
from scipy.signal import kaiserord, lfilter, firwin, freqz, remez
from pylab import figure, clf, plot, subplot, xlabel, ylabel, xlim, ylim, title, grid, axes, show

if __name__ == "__main__":
    x = loadtxt('noisy_ecg.csv', delimiter=",")
    len_ekg = len(x)
    t = linspace(0, len_ekg, len_ekg)

    sample_rate = 1000
    cutoff_hz = 250
    stop_hz = 50
    stop_width_hz = 2

    # ------------------------------------------------
    # Create a FIR filter and apply it to x.
    # ------------------------------------------------

    # The Nyquist rate of the signal.
    nyq_rate = sample_rate / 2.0

    # The desired width of the transition from pass to stop,
    # relative to the Nyquist rate.  We'll design the filter
    # with a 5 Hz transition width.
    width = 5.0 / nyq_rate

    # The desired attenuation in the stop band, in dB.
    ripple_db = 60.0

    # Compute the order and Kaiser parameter for the FIR filter.
    N, beta = kaiserord(ripple_db, width)

    # Use firwin with a Kaiser window to create a lowpass FIR filter.
    taps = firwin(N, cutoff_hz / nyq_rate, window=('kaiser', beta))

    width = 5.0 / nyq_rate
    N, beta = kaiserord(ripple_db, width)

    # Band stop filter
    taps2 = firwin(N, [(stop_hz - stop_width_hz) / nyq_rate, (stop_hz + stop_width_hz) / nyq_rate])

    # Use lfilter to filter x with the FIR filter.
    filtered_x = lfilter(taps, 1.0, x)
    filtered_x = lfilter(taps2, 1.0, filtered_x)

    # ------------------------------------------------
    # Plot the FIR filter coefficients.
    # ------------------------------------------------

    figure(1)
    subplot(211)
    plot(taps, 'bo-', linewidth=2)
    title('Filter Coefficients - low pass (%d taps)' % len(taps))
    grid(True)

    subplot(212)
    plot(taps2, 'bo-', linewidth=2)
    title('Filter Coefficients - band stop (%d taps)' % len(taps2))
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
    delay = 0.5 * (N - 1) / sample_rate

    figure(4)
    # Plot the original signal.
    plot(t, x)
    # Plot the filtered signal, shifted to compensate for the phase delay.
    plot(t - delay, filtered_x, 'r-')
    # Plot just the "good" part of the filtered signal.  The first N-1
    # samples are "corrupted" by the initial conditions.
    plot(t[N - 1:] - delay, filtered_x[N - 1:], 'g', linewidth=4)

    xlabel('t')
    grid(True)

    show()
