from aiogram import Bot, Dispatcher
from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram.filters import Command
from config import Config
from bot.handlers import (
    handle_text,
    handle_photo,
    handle_document,
    cmd_start,
    cmd_help
)
import asyncio
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher()

    # Регистрация обработчиков команд
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_help, Command("help"))

    # Регистрация обработчиков контента
    dp.message.register(handle_text)
    dp.message.register(handle_photo, ContentType.PHOTO)
    dp.message.register(handle_document, ContentType.DOCUMENT)

    try:
        logger.info("Бот успешно запущен")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())