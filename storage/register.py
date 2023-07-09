import os
import common.wavfile as wavfile

from storage.database import database
from common.fingerprint import fingerprint

def register_directory(db, wav_path, txt_path):
    wav_files = os.listdir(wav_path)
    wav_files = [file for file in wav_files if file.endswith('.wav')]

    txt_files = os.listdir(txt_path)
    txt_files = [file for file in txt_files if file.endswith('.txt')]
    
    for wav_file in wav_files:
        samples, samplerate = wavfile.open(os.path.join(wav_path, wav_file))
        hashes, timestamps = fingerprint(samples, samplerate)
    
        info = "Unknown"
        for txt_file in txt_files:
            if os.path.splitext(txt_file)[0] == os.path.splitext(wav_file)[0]:
                info = open(os.path.join(txt_path, txt_file), 'r').read()

        db.insert(hashes, timestamps, wav_file, info)

