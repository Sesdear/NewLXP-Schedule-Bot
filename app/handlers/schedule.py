from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from api.schedule import *



from database import Utils
from datetime import datetime, timedelta
import logging, os

router = Router()


@router.message(Command("schedule"))
async def cmd_schedule(message: Message):
    
    tg_chat_id = message.chat.id
    if tg_chat_id != int(os.getenv("TELEGRAM_CHAT_ID", 0)):
        await message.answer("Неавторизованный чат, обратитесь к администрартору бота")
        return
    
    utils = Utils()
    utils.email = os.getenv("NEWLXP_EMAIL", "")
    if not utils.email:
        await message.answer("❌ Бот не настроен: отсутствует NEWLXP_EMAIL")
        return
    token = utils.get_token()
    
    if not token:
        await message.answer("❌ Вы не авторизованы")
        return

    await message.answer("⏳ Получаю расписание на неделю...")

    try:
        today = datetime.now().date()
        week_later = today + timedelta(days=7)

        classes = get_schedule(
            token=token,
            date_from=today.isoformat(),
            date_to=week_later.isoformat()
        )

        text = format_schedule_message(classes, today.isoformat())
        await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)

    except Exception as e:
        logging.exception("Ошибка при получении расписания")
        await message.answer(f"❌ Не удалось получить расписание")
