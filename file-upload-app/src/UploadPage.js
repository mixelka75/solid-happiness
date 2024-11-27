// UploadPage.js
import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import styles from "./UploadPage.module.css";
import { FaCloudUploadAlt } from "react-icons/fa";

function UploadPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setUploadProgress(0);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Пожалуйста, выберите файл для загрузки.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setUploadProgress(progress);
        },
      });

      const { filename } = response.data;
      navigate(`/status/${filename}`);
    } catch (error) {
      console.error("Ошибка при загрузке файла:", error);
      alert("Произошла ошибка при загрузке файла.");
    }
  };

  return (
    <main className={styles.container}>
      <h1 className={styles.title}>
        <FaCloudUploadAlt /> Загрузка файла
      </h1>
      <div className={styles.inputWrapper}>
        <input type="file" onChange={handleFileChange} />
        <button
          className={styles.button}
          onClick={handleUpload}
          aria-label="Загрузить файл"
        >
          Загрузить
        </button>
      </div>
      {uploadProgress > 0 && (
        <div className={styles.progressBar}>
          <div style={{ width: `${uploadProgress}%` }}></div>
          <div className={styles.progressText}>{uploadProgress}%</div>
        </div>
      )}
    </main>
  );
}

export default UploadPage;
