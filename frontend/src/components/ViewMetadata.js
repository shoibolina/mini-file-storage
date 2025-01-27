import React, { useState, useEffect } from "react";
import axios from "axios";

function ViewMetadata() {
  const [metadata, setMetadata] = useState([]);

  useEffect(() => {
    const fetchMetadata = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/metadata");
        setMetadata(response.data);
      } catch (error) {
        console.error("Error fetching metadata.");
      }
    };

    fetchMetadata();
  }, []);

  return (
    <div>
      <h2>View Metadata</h2>
      <table border="1">
        <thead>
          <tr>
            <th>File Name</th>
            <th>Chunk ID</th>
            <th>Node</th>
            <th>Replica Node</th>
          </tr>
        </thead>
        <tbody>
          {metadata.map((row, index) => (
            <tr key={index}>
              <td>{row[0]}</td>
              <td>{row[1]}</td>
              <td>{row[2]}</td>
              <td>{row[3]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ViewMetadata;
