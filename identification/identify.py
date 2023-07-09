import numpy as np
import pyaudio

import common.wavfile as wavfile
from storage.database import database
from common.fingerprint import fingerprint
from common.settings import (BIN_WIDTH,
                             DEFAULT_TOP_MATCHES,
                             CONFIDENCE_BASE)


def print_matches(matches):
    for match in matches:
        print(f"Name: {match[0]}")
        print(f"Confidence: {match[1]}")
        print(f"Time: {'seconds ,'.join(str(offset) for offset in match[2])}")
        print(f"Info: {match[3]}")

def identify_microphone(db, duration):
    format = pyaudio.paInt16
    channels = 1
    audio = pyaudio.PyAudio()
    samplerate = 44100

    buffer_size = int(samplerate * duration)

    stream = audio.open(format=format, 
                        channels=channels,
                        rate=samplerate, input=True,
                        frames_per_buffer=buffer_size)
    
    buffer = stream.read(buffer_size)

    stream.stop_stream()
    stream.close()

    samples = np.frombuffer(buffer, dtype=np.int16)

    return _identify(db, samples, samplerate)

def identify_file(db, path):
    samples, samplerate = wavfile.open(path)
    return _identify(db, samples, samplerate)

def _rank_matches(matches, top_matches):
    sorted_matches = sorted(matches, key=lambda x: x[1], reverse=True)

    if len(matches) < top_matches:
        top = sorted_matches[0:len(matches)]
    else:
        top = sorted_matches[0:top_matches]
    
    return zip(*top)

def _histogram_rating(offsets):
    range = np.arange(np.min(offsets), np.max(offsets) + BIN_WIDTH, BIN_WIDTH)

    histogram = np.histogram(offsets, bins=range)[0]
    max = np.max(histogram, initial=0)

    offsets_indices = np.where(max == histogram)
    offsets = np.take(range, offsets_indices)

    return max, offsets

def _identify(db, samples, samplerate, top_matches = DEFAULT_TOP_MATCHES):
    hashes, timestamps = fingerprint(samples, samplerate)
    matches = db.search_hashes(hashes, timestamps)

    results = []
    best_rating = 0
    for key in matches.keys():
        if len(matches[key]) < best_rating:
            continue

        rating, offsets = _histogram_rating(matches[key])

        if rating > best_rating:
            best_rating = rating

        """Would be better if confidence was relative to other matches, but this is quick and easy"""
        confidence = 1 - CONFIDENCE_BASE**(-rating)

        results.append([key, confidence, offsets])
    
    top_ids, top_confidences, top_offsets = _rank_matches(results, top_matches)
    top_info = db.search_info(top_ids)

    return list(zip(top_ids, top_confidences, top_offsets, top_info))