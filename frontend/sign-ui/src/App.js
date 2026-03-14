import React, { useRef, useState } from "react";
import Webcam from "react-webcam";
import axios from "axios";

function App() {
  const webcamRef = useRef(null);
  const [detected, setDetected] = useState("");

  const capture = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    const response = await axios.post("http://localhost:8000/predict", {
      image: imageSrc,
    });
    setDetected(response.data.prediction);
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h1>Sign Language Translator</h1>
      <Webcam audio={false} ref={webcamRef} screenshotFormat="image/jpeg" width={500} />
      <button onClick={capture}>Capture</button>
      <h2>Detected Text:</h2>
      <p>{detected}</p>
    </div>
  );
}

export default App;