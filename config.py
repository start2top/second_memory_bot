import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

class Config:
    # Telegram
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Токен бота из .env
    
    # Google Sheets
    GOOGLE_CREDS = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json")  # Путь к JSON
    SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "Вторая память")  # Название таблицы
    SHEET_PAGE = os.getenv("GOOGLE_SHEET_PAGE", "Данные")  # Название листа
    
    # OpenAI
    OPENAI_KEY = os.getenv("OPENAI_API_KEY")  # Ключ API OpenAI
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # Модель GPT