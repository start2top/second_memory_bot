import openai
from config import Config

openai.api_key = Config.OPENAI_KEY

def analyze_text(text: str) -> dict:
    """Анализирует текст и возвращает структурированные данные"""
    response = openai.ChatCompletion.create(
        model=Config.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Извлеки суть текста. Верни JSON: {type, summary, tags[], text}. Теги на русском."
            },
            {"role": "user", "content": text}
        ],
        temperature=0.3
    )
    return eval(response.choices[0].message['content'])


def analyze_image(file_id: str) -> dict:
    """Анализирует изображение через Vision API"""
    # Реализация обработки фото
    pass

def analyze_document(file_id: str) -> dict:
    """Извлекает текст из документов"""
    # Реализация обработки документов
    pass


    