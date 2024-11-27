// App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import UploadPage from "./UploadPage";
import StatusPage from "./StatusPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UploadPage />} />
        <Route path="/status/:filename" element={<StatusPage />} />
      </Routes>
    </Router>
  );
}

export default App;
