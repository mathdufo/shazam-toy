DEFAULT_DB_PATH = "shazam-toy.db"

"""Number of matched audio to return"""
DEFAULT_TOP_MATCHES = 1

"""Used to compute the confidence of a match. n in 1 - n^(-x)."""
CONFIDENCE_BASE = 1.1

"""Size of the bins in the hisogram"""
BIN_WIDTH = 0.25

"""Size of the window in computation of spectrograms"""
FFT_WINDOW_SIZE = 4096

"""Ratio of overlap between windows in computation of spectrograms"""
FFT_OVERLAP_RATIO = 0

"""Size of the maximum filter used to find peaks in the fingerprinting process. 2x more = higher accuracy and 4x lower speed."""
MAXIMUM_FILTER_SIZE = 16

"""Number of pair for each peak. More = higher accuracy and lower speed"""
PAIRS_PER_PEAK = 5