from config import Config
import gspread
from google.oauth2.service_account import Credentials

def save_to_sheet(data: dict):
    """Структурированное сохранение данных"""
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file(Config.GOOGLE_CREDS, scopes=scope)
    gc = gspread.authorize(creds)
    
    sheet = gc.open(Config.SHEET_NAME).worksheet(Config.SHEET_PAGE)  # Исправлено worksheet -> worksheet
    
    sheet.append_row([
        data.get('type', ''),
        data.get('description', ''),
        data.get('tags', ''),
        data.get('raw_text', '')[:500]  # Добавлена закрывающая скобка
    ])  # Исправлено - добавлена закрывающая скобка для append_row