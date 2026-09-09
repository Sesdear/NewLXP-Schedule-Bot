from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import os, logging

router = Router()

# Set your WebApp URL (Must be HTTPS, e.g., ngrok or your domain)
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://your-domain.com")

@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.chat.id != int(os.getenv("TELEGRAM_CHAT_ID", 0)):
        await message.answer("Неавторизованный чат, обратитесь к администратору бота")
        logging.error(f"Unauthorized chat id: {message.chat.id}")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔑 Войти в LXP",
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ]
        ]
    )

    await message.answer(
        "NewLxp бот для получения расписания", 
        reply_markup=keyboard
    )