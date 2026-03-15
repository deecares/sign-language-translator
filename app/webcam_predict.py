from operator import ne

import cv2
import numpy as np
import tensorflow as tf
import pyttsx3
import time
engine = pyttsx3.init()

word = ""
last_letter = ""
last_added_time = 0
# load trained model
model = tf.keras.models.load_model("model/model.h5")
prediction_buffer = []

labels = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    roi = frame[100:300, 100:300]
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)

    img = cv2.resize(roi, (64,64))
    img = img / 255.0
    img = np.reshape(img, (1,64,64,3))

    prediction = model.predict(img, verbose=0)
    confidence = np.max(prediction)
    pred_letter = labels[np.argmax(prediction)]

    if confidence > 0.8:
        prediction_buffer.append(pred_letter)

        if len(prediction_buffer) > 15:
            prediction_buffer.pop(0)

        letter = max(set(prediction_buffer), key=prediction_buffer.count)
    else:
        letter = "?"
    current_time = time.time()

    if letter != last_letter and confidence > 0.8:
        if current_time - last_added_time > 1.5:
            word += letter
            last_letter = letter
            last_added_time = current_time

    cv2.rectangle(frame,(100,100),(300,300),(0,255,0),2)
    cv2.putText(frame, letter, (100,90),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,(0,255,0),2)
    cv2.putText(frame, "Word: " + word, (50,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1, (255,0,0), 2)

    cv2.imshow("Sign Language Detection", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    if key == ord('s'):
        engine.say(word)
        engine.runAndWait()

    if key == ord('c'):
        word = ""

cap.release()
cv2.destroyAllWindows()
