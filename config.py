import os

class Config:
    SECRET_KEY = 'this_is_a_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'  # Или ваша база данных
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'  # Путь для загрузки файлов
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # Ограничение на размер файла (50MB)
