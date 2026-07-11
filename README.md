# 🤟 Sign Language to Text & Speech Translator

An AI-powered web application that recognizes American Sign Language (ASL) hand gestures and converts them into readable text and speech in real time. The project leverages Deep Learning and Computer Vision to improve communication between sign language users and non-signers.

## 🚀 Features

- 🖐️ Real-time sign language gesture recognition
- 📝 Converts sign language into text
- 🔊 Text-to-Speech (TTS) output
- 📷 Webcam-based gesture detection
- 🤖 Deep Learning model for accurate classification
- 💻 User-friendly web interface

## 🛠️ Tech Stack

- Python
- TensorFlow / Keras
- OpenCV
- NumPy
- Flask
- HTML
- CSS
- JavaScript
- gTTS (Google Text-to-Speech)

## 🧠 Model

The gesture recognition model is built using a **Convolutional Neural Network (CNN)** trained on the **American Sign Language (ASL) Alphabet Dataset**.

### Model Performance

- **Model:** CNN
- **Dataset:** ASL Alphabet Dataset
- **Accuracy:** **72%**
- **Framework:** TensorFlow/Keras

## 📂 Project Structure

```text
Sign-Language-Translator/
│── app.py
│── model/
│── static/
│── templates/
│── dataset/
│── requirements.txt
│── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/deecares/sign-language-translator.git
cd sign-language-translator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

## 🎯 How It Works

1. Capture hand gestures using a webcam.
2. Preprocess the captured image.
3. Feed the image into the trained CNN model.
4. Predict the corresponding ASL alphabet.
5. Display the translated text.
6. Convert the text into speech using Text-to-Speech.

## 💡 Future Enhancements

- Support complete words and sentences
- Dynamic gesture recognition
- Multiple sign language support
- Improved model accuracy
- Mobile application
- Voice-to-Sign translation
- Cloud deployment

## 📚 Applications

- Assistive communication for deaf and hard-of-hearing individuals
- Educational tools for learning sign language
- Accessibility solutions
- Healthcare and customer service support

## 👩‍💻 Author

**Deekshitha Marothu**

- GitHub: https://github.com/deecares

## 📄 License

This project is developed for educational and research purposes.
