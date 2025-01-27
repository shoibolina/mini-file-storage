import React, { useState } from "react";
import axios from "axios";

function RecoverData() {
  const [message, setMessage] = useState("");

  const handleRecoverData = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/recover");
      setMessage(response.data.message);
    } catch (error) {
      setMessage("Error recovering data.");
    }
  };

  return (
    <div>
      <h2>Recover Data</h2>
      <button onClick={handleRecoverData}>Recover Data</button>
      <p>{message}</p>
    </div>
  );
}

export default RecoverData;
