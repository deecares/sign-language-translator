import cv2
import numpy as np
import tensorflow as tf

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

    if len(prediction_buffer) > 0:
        letter = max(set(prediction_buffer), key=prediction_buffer.count)
    else:
        letter = "?"

    cv2.rectangle(frame,(100,100),(300,300),(0,255,0),2)
    cv2.putText(frame, letter, (100,90),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,(0,255,0),2)

    cv2.imshow("Sign Language Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
