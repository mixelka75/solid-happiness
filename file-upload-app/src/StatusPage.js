// StatusPage.js
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import styles from "./StatusPage.module.css";
import { FaCheckCircle } from "react-icons/fa";

function StatusPage() {
  const { filename } = useParams();
  const [status, setStatus] = useState("");
  const [downloadLink, setDownloadLink] = useState("");

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await axios.get(`/status/${filename}`);
        const { status } = response.data;

        if (status.startsWith("/download/")) {
          const backendUrl = "http://localhost:8000"; // Замените на ваш URL бэкенда, если он другой
          setDownloadLink(`${backendUrl}${status}`);
        } else {
          setStatus(status);
        }
      } catch (error) {
        console.error("Ошибка при получении статуса:", error);
        setStatus("Ошибка при получении статуса");
      }
    };

    fetchStatus();

    const intervalId = setInterval(() => {
      fetchStatus();
    }, 5000);

    return () => clearInterval(intervalId);
  }, [filename]);

  if (downloadLink) {
    return (
      <main className={styles.container}>
        <h1 className={styles.title}>
          <FaCheckCircle /> Файл готов!
        </h1>
        <a href={downloadLink} download>
          <button className={styles.button} aria-label="Скачать файл">
            Скачать файл
          </button>
        </a>
      </main>
    );
  }

  return (
    <main className={styles.container}>
      <h1 className={styles.title}>Обработка файла</h1>
      <div className={styles.spinner}></div>
      <p className={styles.statusText}>Текущий статус: {status}</p>
    </main>
  );
}

export default StatusPage;
