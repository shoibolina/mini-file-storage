import React, { useState } from "react";
import axios from "axios";

function DownloadFile() {
  const [fileName, setFileName] = useState("");
  const [message, setMessage] = useState("");

  const handleDownload = async () => {
    if (!fileName) {
      setMessage("Please enter a file name.");
      return;
    }

    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/download/${fileName}`,
        { responseType: "blob" }
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", fileName);
      document.body.appendChild(link);
      link.click();

      setMessage("File downloaded successfully.");
    } catch (error) {
      setMessage("Error downloading file.");
    }
  };

  return (
    <div>
      <h2>Download File</h2>
      <input
        type="text"
        placeholder="Enter file name"
        value={fileName}
        onChange={(e) => setFileName(e.target.value)}
      />
      <button onClick={handleDownload}>Download</button>
      <p>{message}</p>
    </div>
  );
}

export default DownloadFile;
