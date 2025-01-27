import React, { useState } from "react";
import axios from "axios";

function SimulateNodeFailure() {
  const [node, setNode] = useState("");
  const [message, setMessage] = useState("");

  const handleSimulateFailure = async () => {
    if (!node) {
      setMessage("Please enter a node name.");
      return;
    }

    try {
      const response = await axios.post(
        `http://127.0.0.1:5000/simulate_failure/${node}`
      );
      setMessage(response.data.message);
    } catch (error) {
      setMessage("Error simulating node failure.");
    }
  };

  return (
    <div>
      <h2>Simulate Node Failure</h2>
      <input
        type="text"
        placeholder="Enter node name (e.g., node1)"
        value={node}
        onChange={(e) => setNode(e.target.value)}
      />
      <button onClick={handleSimulateFailure}>Simulate Failure</button>
      <p>{message}</p>
    </div>
  );
}

export default SimulateNodeFailure;
