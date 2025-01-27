import React from "react";
import UploadFile from "./components/UploadFile";
import DownloadFile from "./components/DownloadFile";
import SimulateNodeFailure from "./components/SimulateNodeFailure";
import RecoverData from "./components/RecoverData";
import ViewMetadata from "./components/ViewMetadata";

function App() {
  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Distributed File Storage System</h1>
      <UploadFile />
      <DownloadFile />
      <SimulateNodeFailure />
      <RecoverData />
      <ViewMetadata />
    </div>
  );
}

export default App;
