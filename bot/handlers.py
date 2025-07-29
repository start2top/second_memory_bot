from aiogram.types import Message, PhotoSize, Document
from aiogram.filters import Command
from services.openai_client import analyze_text, analyze_image, analyze_document
from services.google_sheets import save_to_sheet
import logging

logger = logging.getLogger(__name__)

async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        "📚 Бот 'Вторая память'\n\n"
        "Отправьте мне:\n"
        "- Текст - для анализа и сохранения\n"
        "- Фото - для распознавания текста\n"
        "- Документ (PDF/TXT/DOCX) - для извлечения содержимого"
    )

async def cmd_help(message: Message):
    """Обработчик команды /help"""
    await message.answer(
        "ℹ️ Помощь по использованию:\n\n"
        "1. Просто отправьте текст - я его проанализирую и сохраню\n"
        "2. Отправьте фото с текстом - я распознаю и сохраню текст\n"
        "3. Отправьте документ - я извлеку и сохраню содержимое\n\n"
        "Все данные сохраняются в структурированном виде!"
    )

async def handle_text(message: Message):
    """Обработчик текстовых сообщений"""
    try:
        logger.info(f"Получен текст от пользователя {message.from_user.id}")
        
        analysis = analyze_text(message.text)
        
        data = {
            "type": "Текст",
            "description": analysis['summary'],
            "tags": ", ".join(analysis['tags']),
            "raw_text": message.text[:1000]  # Ограничение длины
        }
        
        save_to_sheet(data)
        
        await message.reply(
            f"✅ Сохранено!\n\n"
            f"📝 Описание: {analysis['summary']}\n"
            f"🏷 Теги: {', '.join(analysis['tags'])}"  # Добавлена закрывающая скобка
        )
    
    except Exception as e:
        logger.error(f"Ошибка обработки текста: {e}")
        await message.reply("❌ Не удалось обработать текст. Попробуйте позже.")

async def handle_photo(message: Message):
    """Обработчик фотографий"""
    try:
        logger.info(f"Получено фото от пользователя {message.from_user.id}")
        
        # Берем фото с самым высоким разрешением
        photo = message.photo[-1]  
        await message.answer("🖼 Обрабатываю изображение...")
        
        # Анализ изображения
        analysis = analyze_image(photo.file_id)
        
        data = {
            "type": "Изображение",
            "description": analysis['summary'],
            "tags": ", ".join(analysis['tags']),
            "raw_text": analysis['extracted_text'][:1000]
        }
        
        save_to_sheet(data)
        
        await message.reply(
            f"✅ Изображение обработано!\n\n"
            f"📝 Описание: {analysis['summary']}\n"
            f"🏷 Теги: {', '.join(analysis['tags'])}\n"  # Добавлена закрывающая скобка
            f"📖 Текст: {analysis['extracted_text'][:300]}..."
        )
    
    except Exception as e:
        logger.error(f"Ошибка обработки фото: {e}")
        await message.reply("❌ Не удалось обработать изображение.")

async def handle_document(message: Message):
    """Обработчик документов с проверкой типа файла"""
    try:
        doc = message.document
        logger.info(f"Получен документ {doc.file_name} от {message.from_user.id}")

        # Проверяем расширение файла
        if not doc.file_name:
            await message.reply("❌ Файл без имени не поддерживается")
            return

        file_ext = doc.file_name.lower().split('.')[-1]
        supported_ext = ['pdf', 'txt', 'docx', 'doc']
        
        if file_ext not in supported_ext:
            await message.reply(
                f"❌ Формат .{file_ext} не поддерживается.\n"
                f"📌 Отправьте файл в одном из форматов: {', '.join(supported_ext)}"
            )
            return

        await message.answer(f"📄 Обрабатываю документ {doc.file_name}...")
        
        try:
            # Анализ документа
            analysis = analyze_document(doc.file_id)
            
            data = {
                "type": f"Документ ({doc.file_name})",
                "description": analysis['summary'],
                "tags": ", ".join(analysis['tags']),
                "raw_text": analysis['extracted_text'][:1000]  # Ограничение длины
            }
            
            save_to_sheet(data)
            
            await message.reply(
                f"✅ Документ обработан!\n\n"
                f"📝 Описание: {analysis['summary']}\n"
                f"🏷 Теги: {', '.join(analysis['tags'])}\n"
                f"📖 Текст: {analysis['extracted_text'][:300]}..."
            )
            
        except Exception as analysis_error:
            logger.error(f"Ошибка анализа документа: {analysis_error}")
            await message.reply("❌ Ошибка при анализе документа. Попробуйте другой файл.")

    except Exception as e:
        logger.error(f"Общая ошибка обработки документа: {e}")
        await message.reply("❌ Не удалось обработать документ. Попробуйте позже.")