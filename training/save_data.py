import csv
from datetime import datetime

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import sklearn.model_selection as model_selection

from main import SAMPLE_RATE


def get_metadata():
    reader = csv.reader(open('maestro-v3.0.0.csv', encoding="'utf-8'"), skipinitialspace=True)
    metadata = np.array(list(reader)).astype('str')
    metadata = np.delete(metadata, [1, 3, 4], 1)

    # only keep most common 10 composers
    # by frequency (most popular to least):  Chopin, Schubert, Beethoven, Bach, Liszt, Rachmaninoff, Schumann, Debussy, Haydn, Mozart
    # by output order:  Debussy, Liszt, Schubert, Chopin, Bach, Haydn, Beethoven, Schumann, Rachmaninoff, Mozart
    unique_composers, frequency = np.unique(metadata[:, 0], return_counts=True)
    sorted_indexes = np.argsort(frequency)[::-1]
    sorted_by_freq = unique_composers[sorted_indexes]
    metadata = metadata[np.in1d(metadata[:, 0], sorted_by_freq[:10])]
    print(np.unique(metadata[:, 0]))
    return metadata


def get_spectrogram(track_id, start_time=0):
    y, sr = librosa.load(f'maestro-{SAMPLE_RATE}\{track_id}', sr=None, offset=start_time, duration=30)
    # y, sr = librosa.load(f'D:\maestro-v3.0.0\{track_id}', sr=None, duration=30)
    spect = librosa.feature.melspectrogram(y=y, sr=sr)
    spect_db = librosa.power_to_db(spect, ref=np.max)
    return spect_db


def plot_spectrogram(track_id, start_time=0):
    spect = get_spectrogram(track_id, start_time)
    print(spect.shape)
    librosa.display.specshow(spect, sr=SAMPLE_RATE, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')

plot_spectrogram('2008/MIDI-Unprocessed_09_R1_2008_01-05_ORIG_MID--AUDIO_09_R1_2008_wav--3.wav')

# metadata = get_metadata()
# x = np.stack([get_spectrogram(track_id) for track_id in metadata[:, 2]])
# x = (x + 80) / 80

def get_xy(metadata):
    duration_col = metadata[:, -1].astype(float).astype(int)
    total_samples = sum(duration_col // 30)
    s = get_spectrogram(metadata[0, 2])
    x = np.zeros((total_samples, s.shape[0], s.shape[1]))

    sample_ct = 0
    for i, track_id in enumerate(metadata[:, 2]):
        for clip_start in range(0, duration_col[i] - 29, 30):
            x[sample_ct] = get_spectrogram(track_id, start_time=clip_start)
            sample_ct += 1
            print(f'{datetime.now().strftime("%H:%M:%S")} - CONVERTED SAMPLE {sample_ct}/{total_samples}')

    x = (x + 80) / 80

    composers = np.unique(metadata[:, 0])
    composer_sample_ct = sum(duration_col[metadata[:, 0] == composers[0]] // 30)
    y = np.array([composers[0]] * composer_sample_ct)
    for composer in composers[1:]:
        composer_sample_ct = sum(duration_col[metadata[:, 0] == composer] // 30)
        y = np.concatenate((y, np.array([composer] * composer_sample_ct)))

    ohe = OneHotEncoder(sparse=False)
    y = ohe.fit_transform(y[:, np.newaxis])

    return x, y

metadata = get_metadata()

print('\n==== TRAINING DATA ====')
x_train, y_train = get_xy(metadata[metadata[:, 1] == 'train'])
print('\n==== VALIDATION DATA ====')
x_validation, y_validation = get_xy(metadata[metadata[:, 1] == 'validation'])
print('\n==== TEST DATA ====')
x_test, y_test = get_xy(metadata[metadata[:, 1] == 'test'])

# x, y = get_xy(metadata)
#
# x_train, x_temp, y_train, y_temp = model_selection.train_test_split(x, y, test_size=0.20, random_state=1)
# x_test, x_val, y_test, y_val = model_selection.train_test_split(x_temp, y_temp, test_size=0.50, random_state=1)


# train_slice, validation_slice, test_slice = metadata[:, 1] == 'train', metadata[:, 1] == 'validation', metadata[:, 1] == 'test'
# x_train, x_validation, x_test = x[train_slice], x[validation_slice], x[test_slice]
# y_train, y_validation, y_test = y[train_slice], y[validation_slice], y[test_slice]

# x_train = x[metadata[:, 1] == 'train']
# x_validation = x[metadata[:, 1] == 'validation']
# x_test = x[metadata[:, 1] == 'test']
#
# y_train = y[metadata[:, 1] == 'train']
# y_validation = y[metadata[:, 1] == 'validation']
# y_test = y[metadata[:, 1] == 'test']

# np.save(f'x_train_{SAMPLE_RATE}.npy', x_train)
# np.save(f'x_validation_{SAMPLE_RATE}.npy', x_validation)
# np.save(f'x_test_{SAMPLE_RATE}.npy', x_test)
# np.save(f'y_train.npy', y_train)
# np.save(f'y_validation.npy', y_validation)
# np.save(f'y_test.npy', y_test)

np.savez(f'maestro_{SAMPLE_RATE}_4.npz',
         x_train=x_train, x_val=x_validation, x_test=x_test,
         y_train=y_train, y_val=y_validation, y_test=y_test)
