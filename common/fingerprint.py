import matplotlib.pyplot as plt
import numpy as np
import scipy

from common.settings import (FFT_WINDOW_SIZE,
                      FFT_OVERLAP_RATIO,
                      MAXIMUM_FILTER_SIZE,
                      PAIRS_PER_PEAK)

def fingerprint(samples, samplerate, plot:bool=False):
    spectrogram, frequencies, times = spectrograph(samples, samplerate, plot=plot)
    peaks = get_peaks(spectrogram, frequencies, times, plot=plot)

    return hash_peaks(peaks)

def spectrograph(samples, samplerate, plot:bool=False):
    frequencies, times, spectrogram = scipy.signal.spectrogram(samples, 
                                           fs=samplerate, 
                                           window = np.hanning(FFT_WINDOW_SIZE),
                                           noverlap = int(FFT_OVERLAP_RATIO * FFT_WINDOW_SIZE),
                                           nfft = FFT_WINDOW_SIZE)

    if plot:
        plt.imshow(10 * np.log10(spectrogram, where=(spectrogram != 0)))
        plt.title("Spectrogram")
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.show()
    
    return spectrogram, frequencies, times

def get_peaks(spectrogram, frequencies, times, plot = False):
    peaks = scipy.ndimage.maximum_filter(spectrogram, MAXIMUM_FILTER_SIZE) == spectrogram
    frequencies_idx, times_idx = np.where(peaks)

    if plot:
        plt.imshow(10 * np.log10(spectrogram, where=(spectrogram != 0)))
        plt.plot(times_idx, frequencies_idx, ".r")
        plt.title("Spectrogram")
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.show()

    frequencies = np.take(frequencies, frequencies_idx)
    times = np.take(times, times_idx)
    peaks = np.column_stack((times, frequencies))
    #Sort along the time axis
    peaks = peaks[peaks[:,0].argsort()].round(decimals=3)

    return peaks

def hash_peaks(peaks):
    hashes = []
    timestamps = []
    
    for i in range(peaks.shape[0] - PAIRS_PER_PEAK):
        for j in range (1, PAIRS_PER_PEAK):
            t1 = peaks[i, 0]
            t2 = peaks[i+j, 0]

            f1 = peaks[i, 1] 
            f2 = peaks[i+j, 1] 
            
            t_delta = np.round(t2-t1, decimals=3)

            hashes.append(f"{f1}|{f2}|{t_delta}")
            timestamps.append(t1)
    
    return hashes, timestamps