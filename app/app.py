from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import librosa
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
import json

app = Flask(__name__)
CORS(app)


def gpu_memory_fix():
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)


def get_spectrogram(uri):
    y, sr = librosa.load(uri[uri.index('U:'):], sr=None, duration=30)
    # y, sr = librosa.load(f'D:\maestro-v3.0.0\{track_id}', sr=None, duration=30)
    spect = librosa.feature.melspectrogram(y=y, sr=sr)
    spect_db = librosa.power_to_db(spect, ref=np.max)
    spect_db = (spect_db + 80) / 80
    return spect_db


def run_model(uri):
    spect = get_spectrogram(uri)
    model = keras.models.load_model('C:/Users/831276/Projects/Composer Classification/app/model3.h5')
    confidences = model.predict(spect[None, ..., np.newaxis])[0]
    labels = np.array(
        ['Debussy', 'Liszt', 'Schubert', 'Chopin', 'Bach', 'Haydn', 'Beethoven', 'Schumann', 'Rachmaninoff', 'Mozart'])
    order = np.argsort(-confidences)
    labels, confidences = labels[order], confidences[order] * 100
    results = dict(zip(labels, np.around(confidences.astype(float), 2)))
    results = json.dumps(results)
    print(results)
    return results


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        print('Incoming..')
        return run_model(request.get_json()['uri'])

if __name__ == '__main__':
    app.run(host='192.168.1.237', port=5000)
