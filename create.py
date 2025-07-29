import os
from pathlib import Path

def create_project_structure(base_dir="second_memory_bot"):
    """Создает структуру проекта для бота 'Вторая память'"""
    
    # Создаем базовую директорию
    base_path = Path(base_dir)
    base_path.mkdir(exist_ok=True)
    
    # Создаем файлы в корне
    (base_path / ".env").touch()
    (base_path / "config.py").touch()
    (base_path / "main.py").touch()
    
    # Создаем поддиректории и их файлы
    dirs = {
        "bot": ["__init__.py", "handlers.py", "keyboards.py"],
        "services": ["__init__.py", "openai_client.py", "google_sheets.py"],
        "utils": ["__init__.py", "text_processing.py"]
    }
    
    for dir_name, files in dirs.items():
        dir_path = base_path / dir_name
        dir_path.mkdir(exist_ok=True)
        
        for file in files:
            (dir_path / file).touch()
    
    print(f"Структура проекта создана в папке: {base_dir}")

if __name__ == "__main__":
    create_project_structure()