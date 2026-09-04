from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from api.schedule import *


from database import Utils
from datetime import datetime, timedelta
import logging, os

router = Router()


@router.message(Command("today"))
async def cmd_today(message: Message):
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

    await message.answer("⏳ Получаю расписание на сегодня...")

    try:

        today_local = datetime.now() + timedelta(hours=7)
        today_str = today_local.date().isoformat()
        tomorrow_str = (today_local + timedelta(days=1)).date().isoformat()

        classes = get_schedule(
            token=token,
            date_from=today_str,
            date_to=tomorrow_str
        )

        if not classes:
            await message.answer("Сегодня пар нет")
            return

        text = format_schedule_today_only(classes, today_str)
        
        await message.answer(
            text,
            parse_mode="HTML",
            disable_web_page_preview=True
        )

    except RuntimeError as e:
        await message.answer(f"❌ Ошибка сервера")
        logging.exception(f"Ошибка сервера {e}")
    except Exception as e:
        logging.exception(f"Ошибка в /today для группы {tg_chat_id}")
        await message.answer("❌ Не удалось получить расписание. Попробуйте позже.")