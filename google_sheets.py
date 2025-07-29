from config import Config
import gspread
from google.oauth2.service_account import Credentials
import os

def test_connection():
    try:
        # 1. Проверка существования файла credentials
        if not os.path.exists(Config.GOOGLE_CREDS):
            return f"Файл {Config.GOOGLE_CREDS} не найден!"
        
        # 2. Проверка доступа к API
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = Credentials.from_service_account_file(
            Config.GOOGLE_CREDS, 
            scopes=scope
        )
        
        print(f"✅ Учётные данные загружены. Email: {creds.service_account_email}")
        
        # 3. Попытка открыть таблицу
        gc = gspread.authorize(creds)
        try:
            sh = gc.open(Config.SHEET_NAME)
            print(f"✅ Таблица '{Config.SHEET_NAME}' найдена")
        except gspread.SpreadsheetNotFound:
            return f"❌ Таблица '{Config.SHEET_NAME}' не найдена!"
        
        # 4. Проверка листа
        try:
            worksheet = sh.worksheet(Config.SHEET_PAGE)
            print(f"✅ Лист '{Config.SHEET_PAGE}' доступен")
        except gspread.WorksheetNotFound:
            return f"❌ Лист '{Config.SHEET_PAGE}' не найден!"
        
        # 5. Тестовая запись
        worksheet.append_row(["Тест", "2024-07-30", "Проверка связи"])
        return "✅ Данные успешно добавлены!"
        
    except Exception as e:
        return f"❌ Критическая ошибка: {str(e)}"

if __name__ == "__main__":
    result = test_connection()
    print(result)