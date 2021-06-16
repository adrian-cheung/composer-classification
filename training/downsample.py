import os
from datetime import datetime
import librosa
import soundfile as sf
from main import SAMPLE_RATE

counter = 1
for root, dirs, files in os.walk('D:\maestro-v3.0.0'):
    if dirs:
        for dir in dirs:
            os.makedirs(f'D:\maestro-{SAMPLE_RATE}\{dir}', exist_ok=True)
        print('CREATED FOLDERS')
    else:
        for file in files:
            if os.path.splitext(file)[1] == '.wav':
                y, sr = librosa.load(f'{root}\{file}')
                sf.write(f'D:\maestro-{SAMPLE_RATE}\{os.path.basename(root)}\{file}', y, SAMPLE_RATE)
                print(
                    f'{datetime.now().strftime("%H:%M:%S")} - RESAMPLED TRACK {counter}/1276 - D:\maestro-{SAMPLE_RATE}\{os.path.basename(root)}\{file}')
                counter += 1

print('SUCCESS')
