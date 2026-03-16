import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# prepare dataset
data = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_data = data.flow_from_directory(
    "dataset/train",
    target_size=(64,64),
    batch_size=8,
    subset="training"
)

val_data = data.flow_from_directory(
    "dataset/train",
    target_size=(64,64),
    batch_size=8,
    subset="validation"
)

# CNN model
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32,(3,3),activation='relu',input_shape=(64,64,3)),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(64,(3,3),activation='relu'),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(128,(3,3),activation='relu'),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128,activation='relu'),
    tf.keras.layers.Dense(26,activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# train model
model.fit(train_data, epochs=10, validation_data=val_data)

# save model
model.save("model.h5")
