import os
import uuid
import threading
import sqlite3
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import main

app = FastAPI()

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'

# Создаем директории для загрузки и результатов, если их нет
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('files.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_status (
            filename TEXT PRIMARY KEY,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Функции для работы с БД
def add_file(filename, status):
    conn = sqlite3.connect('files.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO file_status (filename, status) VALUES (?, ?)', (filename, status))
    conn.commit()
    conn.close()

def update_status(filename, status):
    conn = sqlite3.connect('files.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE file_status SET status=? WHERE filename=?', (status, filename))
    conn.commit()
    conn.close()

def get_status(filename):
    conn = sqlite3.connect('files.db')
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM file_status WHERE filename=?', (filename,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

def delete_file_record(filename):
    conn = sqlite3.connect('files.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM file_status WHERE filename=?', (filename,))
    conn.commit()
    conn.close()

# Инициализация БД при старте приложения
init_db()

# Долгая задача, выполняемая в отдельном потоке
def long_running_process(filename):

    # Создаем результат обработки
    result_filename = f'result_{filename}'
    main.get_gold(filename, result_filename)

    # Обновляем статус на ссылку для скачивания
    download_link = f'/download/{result_filename}'
    update_status(filename, download_link)

# Эндпоинт для загрузки файлов
@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    # Генерируем рандомное имя файла
    extension = os.path.splitext(file.filename)[1]
    random_filename = f"{uuid.uuid4().hex}{extension}"
    upload_path = os.path.join(UPLOAD_FOLDER, random_filename)

    # Сохраняем загруженный файл
    with open(upload_path, 'wb') as f:
        content = await file.read()
        f.write(content)

    # Добавляем запись в БД со статусом 'uploaded'
    add_file(random_filename, 'uploaded')

    # Запускаем долгую задачу в отдельном потоке
    thread = threading.Thread(target=long_running_process, args=(random_filename,))
    thread.start()

    return {'filename': random_filename}

# Эндпоинт для получения статуса файла
@app.get('/status/{filename}')
def get_file_status(filename: str):
    status = get_status(filename)
    if status:
        return {'filename': filename, 'status': status}
    else:
        raise HTTPException(status_code=404, detail='Файл не найден')

# Эндпоинт для скачивания результата
@app.get('/download/{result_filename}')
def download_file(result_filename: str):
    result_filepath = os.path.join(RESULT_FOLDER, result_filename)
    if os.path.exists(result_filepath):
        return FileResponse(path=result_filepath, filename=result_filename)
    else:
        raise HTTPException(status_code=404, detail='Результат не найден')
