import numpy as np
from keras import models, layers
from keras.regularizers import l2
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt

SAMPLE_RATE = 8000

# def main():
data = np.load(f'maestro_{SAMPLE_RATE}_3.npz')
x_train, x_validation, x_test = data['x_train'], data['x_val'], data['x_test']
y_train, y_validation, y_test = data['y_train'], data['y_val'], data['y_test']

x_train, x_validation, x_test = map(lambda x: x[..., np.newaxis], (x_train, x_validation, x_test))

model = models.Sequential([
    # layers.Conv2D(32, (5, 5), strides=(2, 2), activation='relu', input_shape=(128, 469, 1)),
    # layers.MaxPooling2D(pool_size=(2, 4), strides=(2, 4)),
    # layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    # layers.MaxPooling2D(pool_size=(2, 4), strides=(2, 4)),
    # layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
    # layers.MaxPooling2D(pool_size=(2, 4), strides=(2, 4)),
    # layers.Conv2D(32, (5, 5), strides=(2, 2), activation='relu', input_shape=(128, 469, 1)),
    # layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),
    # layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    # layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),
    # layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
    # layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),
    # layers.Conv2D(16, (5, 5), activation='relu', padding='same', input_shape=(128, 469, 1)),
    # layers.MaxPooling2D(pool_size=(2, 4), strides=(2, 4)),
    # layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
    # layers.MaxPooling2D(pool_size=(2, 4), strides=(2, 4)),
    # layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    # layers.Conv2D(96, (3, 3), activation='relu', padding='same'),
    # layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
    # layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),

    # layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=x_train.shape[1:]),
    # layers.MaxPooling2D(pool_size=(2, 4), strides=(2, 4)),
    # layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    # layers.MaxPooling2D(pool_size=(2, 4), strides=(2, 4)),
    # layers.Conv2D(96, (3, 3), activation='relu', padding='same'),
    # layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
    # layers.Flatten(),
    # layers.Dense(512, activation='relu', kernel_regularizer=l2(0.0005)),
    # layers.Dropout(0.5),
    # layers.Dense(512, activation='relu', kernel_regularizer=l2(0.0005)),
    # layers.Dropout(0.5),
    # layers.Dense(10, activation='softmax')

    # layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(128, 469, 1)),
    # layers.MaxPooling2D(pool_size=(2, 4), strides=(2, 4)),
    # layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    # layers.MaxPooling2D(pool_size=(2, 4), strides=(2, 4)),
    # layers.Flatten(),
    # layers.Dense(256, activation='relu', kernel_regularizer=l2(0.0001)),
    # layers.Dropout(0.5),
    # layers.Dense(256, activation='relu', kernel_regularizer=l2(0.0001)),
    # layers.Dropout(0.5),
    # layers.Dense(10, activation='softmax')

    # layers.Conv2D(60, (5, 5), strides=(2, 2), activation='relu', padding='same', input_shape=x_train.shape[1:]),
    # layers.MaxPooling2D(pool_size=(2, 4), strides=(2, 4)),
    # layers.Conv2D(90, (3, 3), activation='relu', padding='same'),
    # layers.MaxPooling2D(pool_size=(2, 4), strides=(2, 4)),
    # layers.Conv2D(120, (3, 3), activation='relu', padding='same'),
    # layers.Conv2D(120, (3, 3), activation='relu', padding='same'),
    # layers.Conv2D(120, (3, 3), activation='relu', padding='same'),
    # layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),
    # layers.Flatten(),
    # layers.Dense(1600, activation='relu', kernel_regularizer=l2(0.001)),
    # layers.Dropout(0.5),
    # layers.Dense(1600, activation='relu', kernel_regularizer=l2(0.001)),
    # layers.Dropout(0.5),
    # layers.Dense(10, activation='softmax')
    layers.Conv2D(32, (5, 5), strides=(2, 2), activation='relu', padding='same', input_shape=x_train.shape[1:]),
    layers.MaxPooling2D(pool_size=(2, 4), strides=(2, 4)),
    layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D(pool_size=(2, 4), strides=(2, 4)),
    layers.Conv2D(96, (3, 3), activation='relu', padding='same'),
    layers.Conv2D(96, (3, 3), activation='relu', padding='same'),
    # layers.Conv2D(120, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
    layers.Flatten(),
    layers.Dense(1600, activation='relu', kernel_regularizer=l2(0.001)),
    layers.Dropout(0.5),
    layers.Dense(1600, activation='relu', kernel_regularizer=l2(0.001)),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')

])

model.summary()

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)
history = model.fit(x_train, y_train, epochs=50, batch_size=64, validation_data=(x_validation, y_validation),
                    callbacks=[es])
test_loss, test_acc = model.evaluate(x_test, y_test)
print('Test Accuracy:', test_acc)

model.save('model3.h5')

fig, ax = plt.subplots(1)
ax.set(title='Model Accuracy', xlabel='Epoch', ylabel='Accuracy')
ax.plot(history.history['accuracy'])
ax.plot(history.history['val_accuracy'])
ax.legend(['Train', 'Test'], loc='best')

fig, ax = plt.subplots(1)
ax.plot(history.history['loss'])
ax.plot(history.history['val_loss'])
ax.set(title='Model Loss', xlabel='Epoch', ylabel='Loss')
ax.legend(['Train', 'Test'], loc='best')

plt.show()

# if __name__ == '__main__':
#     main()
