import numpy as np
import scipy

def open(path):
    samplerate, samples = scipy.io.wavfile.read(path)
    
    """Doesn't support floats"""
    if not np.issubdtype(samples.dtype, np.integer):
        raise ValueError(f"ERROR: This program only support file integer format, {path} has a format of {samples.dtype}")
        
    """compress multiple channels into one"""
    if samples.ndim == 2:
        samples = samples.mean(axis=-1)
    
    return samples, samplerate
