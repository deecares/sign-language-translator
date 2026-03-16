import React, { useRef, useState, useEffect } from "react";
import axios from "axios";
import Webcam from "react-webcam";
import "./App.css";

function App() {
  const webcamRef = useRef(null);
  const [detectedText, setDetectedText] = useState("Nothing yet");
  const [sentence, setSentence] = useState("");

  // Speak text whenever detectedText changes
  useEffect(() => {
    if (detectedText && detectedText !== "Nothing yet") {
      if ("speechSynthesis" in window) {
        const msg = new SpeechSynthesisUtterance(detectedText);
        msg.lang = "en-US";
        window.speechSynthesis.speak(msg);
      }
    }
  }, [detectedText]);

  // Capture image from webcam and send it to the backend for prediction
  const capture = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    console.log("Captured image:", imageSrc);

    if (!imageSrc) {
      setDetectedText("Unable to capture image from webcam.");
      return;
    }

    setDetectedText("Detecting...");

    try {
      const response = await axios.post("http://localhost:5000/predict", { image: imageSrc });
      const { letter, confidence } = response.data;
      const confidencePct = (confidence * 100).toFixed(1);

      setDetectedText(`${letter} (${confidencePct}%)`);

      // Only append to the sentence when the model is reasonably confident.
      if (confidence > 0.55) {
        setSentence((prev) => prev + letter);
      }
    } catch (err) {
      console.error(err);
      setDetectedText("Detection failed. Is the backend running?");
    }
  };

  const addSpace = () => setSentence((prev) => prev + " ");
  const clearSentence = () => setSentence("");
  const removeLast = () => setSentence((prev) => prev.slice(0, -1));

  return (
    <div className="app-container">
      <h1 className="title">Sign Language Translator</h1>

      <div className="card">
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          className="webcam"
        />
        <button className="capture-btn" onClick={capture}>
          Capture
        </button>
      </div>

      <div className="card output-card">
        <h2>Detected Text</h2>
        <p>{detectedText}</p>

        <div className="sentence-row">
          <h2>Sentence</h2>
          <p className="sentence-text">
            {sentence || <em>Start capturing letters ...</em>}
          </p>
        </div>

        <div className="sentence-actions">
          <button className="small-btn" onClick={addSpace}>
            Add Space
          </button>
          <button className="small-btn" onClick={removeLast}>
            Backspace
          </button>
          <button className="small-btn" onClick={clearSentence}>
            Clear
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;