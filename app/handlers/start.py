from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
import os, logging
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.chat.id != int(os.getenv("TELEGRAM_CHAT_ID", 0)):
        await message.answer("Неавторизованный чат, обратитесь к администрартору бота")
        logging.error(f"Unauthorized chat id: {message.chat.id}")
        return
    await message.answer("NewLxp бот для получения расписания")