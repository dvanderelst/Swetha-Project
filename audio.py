import numpy as np
import sounddevice as sound
from scipy.signal import hilbert
from scipy.signal import butter, sosfilt
import sounddevice
import time
from matplotlib import pyplot


def smooth(x, window_len=11, window='hanning'):
    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if window not in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[x[window_len - 1:0:-1], x, x[-2:-window_len - 1:-1]]
    # print(len(s))
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')

    y = np.convolve(w / w.sum(), s, mode='valid')
    return y


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], analog=False, btype='band', output='sos')
    return sos


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    sos = butter_bandpass(lowcut, highcut, fs, order=order)
    y = sosfilt(sos, data)
    return y


def record_binaural(duration=0.5):
    fs = 44100
    recording = sounddevice.rec(int(duration * fs), samplerate=fs, channels=2, blocking=True)
    recording = np.array(recording)
    return recording


def filter(recording, low, high):
    filtered = np.zeros(recording.shape)
    data0 = recording[:, 0]
    data1 = recording[:, 1]
    data0 = butter_bandpass_filter(data0, low, high, 44100)
    data1 = butter_bandpass_filter(data1, low, high, 44100)
    filtered[:, 0] = data0
    filtered[:, 1] = data1
    return filtered


def get_envelopes(recording, window):
    filtered = np.zeros(recording.shape)
    data0 = recording[:, 0]
    data1 = recording[:, 1]
    n = len(data0)

    data0 = np.abs(hilbert(data0))
    data1 = np.abs(hilbert(data1))

    data0 = smooth(data0, window)
    data1 = smooth(data1, window)

    data0 = data0[:n]
    data1 = data1[:n]

    filtered[:, 0] = data0
    filtered[:, 1] = data1
    return filtered


def average_iid(envelopes, left_channel, right_channel):
    left = envelopes[:, left_channel]
    right = envelopes[:, right_channel]

    ratio = left / right
    db = 20 * np.log10(ratio)
    iid = np.mean(db)

    if iid > 0: direction = 'LEFT'
    if iid < 0: direction = 'RIGHT'
    return iid, db, direction


def handle_audio(do_plot=False):
    left_channel = 1
    right_channel = 0

    sound = record_binaural(0.1)
    sound = filter(sound, 200, 8000)
    envelopes = get_envelopes(sound, 200)
    iid, db, direction = average_iid(envelopes, left_channel, right_channel)

    if do_plot:
        pyplot.figure()
        pyplot.subplot(2,1,1)
        pyplot.plot(sound[:, left_channel], alpha=0.5, color='green')
        pyplot.plot(envelopes[:, left_channel], alpha=1, color='green')
        pyplot.plot(sound[:, right_channel], alpha=0.5, color='red')
        pyplot.plot(envelopes[:, right_channel], alpha=1, color='red')
        pyplot.legend(['left', 'left e', 'right', 'right e'])

        pyplot.subplot(2,1,2)
        max = np.max(np.abs(db))
        pyplot.plot(db)
        pyplot.ylim([- max, max])

        pyplot.show()

    return iid, db, direction

# Test audio
#  Andrea SuperBeam USB Headset: Audio (hw:1,0), ALSA (2 in, 2 out)
if __name__ == "__main__":
    devices = sounddevice.query_devices()
    sounddevice.default.device = 6

    print(devices)

    while True:
        iid, db, direction = handle_audio(False)
        print(iid, direction)

# if __name__ == "__main__":
#     left_channel = 1
#     right_channel = 0
#     devices = sounddevice.query_devices()
#     sounddevice.default.device = 6
#     while True:
#         start = time.time()
#         sound = record_binaural(0.1)
#         sound = filter(sound, 100, 1000)
#         envelopes = get_envelopes(sound, 200)
#         iid, direction = average_iid(envelopes, left_channel, right_channel)
#         iid = iid * 1000
#         end = time.time()
#         duration = end - start
#
#         x = '%+2.2f %+2.2f ' % (iid, duration)
#         x = x + direction
#
#         print(x)
