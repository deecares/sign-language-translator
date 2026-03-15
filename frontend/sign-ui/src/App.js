import React, { useRef, useState, useEffect } from "react";
import Webcam from "react-webcam";
import "./App.css";

function App() {
  const webcamRef = useRef(null);
  const [detectedText, setDetectedText] = useState("Nothing yet");

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

  // Capture image from webcam
  const capture = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    console.log("Captured image:", imageSrc);

    // Update detected text (placeholder for backend)
    setDetectedText("Hello! This is the detected text.");
  };

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
      </div>
    </div>
  );
}

export default App;