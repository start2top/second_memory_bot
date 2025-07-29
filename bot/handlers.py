from aiogram.types import Message, PhotoSize, Document
from aiogram.filters import Command
from services.openai_client import analyze_text, analyze_document
from services.google_sheets import save_to_sheet
from utils.text_processing import extract_text_from_image
from aiogram import Bot
import logging
import os

logger = logging.getLogger(__name__)

async def cmd_start(message: Message):
    await message.answer(
        "📚 Бот 'Вторая память'\n\n"
        "Отправьте мне:\n"
        "- Текст - для анализа и сохранения\n"
        "- Фото - для распознавания текста\n"
        "- Документ (PDF/TXT/DOCX) - для извлечения содержимого"
    )

async def cmd_help(message: Message):
    await message.answer(
        "ℹ️ Помощь по использованию:\n\n"
        "1. Просто отправьте текст - я его проанализирую и сохраню\n"
        "2. Отправьте фото с текстом - я распознаю и сохраню текст\n"
        "3. Отправьте документ - я извлеку и сохраню содержимое\n\n"
        "Все данные сохраняются в структурированном виде!"
    )

async def handle_text(message: Message):
    try:
        logger.info(f"Получен текст от пользователя {message.from_user.id}")
        analysis = analyze_text(message.text)

        data = {
            "type": "Текст",
            "description": analysis['summary'],
            "tags": ", ".join(analysis['tags']),
            "raw_text": message.text[:1000]
        }

        save_to_sheet(data)

        await message.reply(
            f"✅ Сохранено!\n\n"
            f"📝 Описание: {analysis['summary']}\n"
            f"🏷 Теги: {', '.join(analysis['tags'])}"
        )

    except Exception as e:
        logger.error(f"Ошибка обработки текста: {e}")
        await message.reply("❌ Не удалось обработать текст. Попробуйте позже.")


async def handle_photo(message: Message, bot: Bot):
    """Обработка фото с OCR и анализом"""
    try:
        logger.info(f"Получено фото от пользователя {message.from_user.id}")
        await message.answer("🖼 Извлекаю текст с изображения...")

        photo: PhotoSize = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        file_path = file_info.file_path
        local_path = f"temp_photo_{message.message_id}.jpg"

        await bot.download_file(file_path, destination=local_path)

        # OCR
        extracted_text = extract_text_from_image(local_path)

        if not extracted_text.strip():
            await message.reply("❌ Не удалось распознать текст на изображении.")
            os.remove(local_path)
            return

        # Анализ текста
        analysis = analyze_text(extracted_text)

        data = {
            "type": "Изображение",
            "description": analysis['summary'],
            "tags": ", ".join(analysis['tags']),
            "raw_text": extracted_text[:1000]
        }

        save_to_sheet(data)

        await message.reply(
            f"✅ Изображение обработано!\n\n"
            f"📝 Описание: {analysis['summary']}\n"
            f"🏷 Теги: {', '.join(analysis['tags'])}\n"
            f"📖 Текст: {extracted_text[:300]}..."
        )

    except Exception as e:
        logger.error(f"Ошибка обработки фото: {e}")
        await message.reply("❌ Не удалось обработать изображение.")
    finally:
        if os.path.exists(local_path):
            os.remove(local_path)


async def handle_document(message: Message):
    try:
        doc: Document = message.document
        logger.info(f"Получен документ {doc.file_name} от {message.from_user.id}")

        if not doc.file_name:
            await message.reply("❌ Файл без имени не поддерживается")
            return

        file_ext = doc.file_name.lower().split('.')[-1]
        supported_ext = ['pdf', 'txt', 'docx', 'doc']

        if file_ext not in supported_ext:
            await message.reply(
                f"❌ Формат .{file_ext} не поддерживается.\n"
                f"📌 Поддерживаются: {', '.join(supported_ext)}"
            )
            return

        await message.answer(f"📄 Обрабатываю документ {doc.file_name}...")

        analysis = analyze_document(doc.file_id)

        data = {
            "type": f"Документ ({doc.file_name})",
            "description": analysis['summary'],
            "tags": ", ".join(analysis['tags']),
            "raw_text": analysis['extracted_text'][:1000]
        }

        save_to_sheet(data)

        await message.reply(
            f"✅ Документ обработан!\n\n"
            f"📝 Описание: {analysis['summary']}\n"
            f"🏷 Теги: {', '.join(analysis['tags'])}\n"
            f"📖 Текст: {analysis['extracted_text'][:300]}..."
        )

    except Exception as e:
        logger.error(f"Общая ошибка обработки документа: {e}")
        await message.reply("❌ Не удалось обработать документ.")
