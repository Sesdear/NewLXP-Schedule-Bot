from api.get_time import get_current_time
from api.schedule import format_schedule_today_only
from api.schedule import get_schedule
from config import TELEGRAM_CHAT_ID
from datetime import datetime, time
from aiogram import Bot, Dispatcher
from datetime import datetime, timedelta
from database import Utils
import os
import logging

async def send_schedule(bot: Bot):
    time_get = await get_current_time()
    if time_get is None:
        return
    time_format = datetime.strptime(time_get, "%H:%M:%S.%f").time()
    
    
    
    if time(6, 0) <= time_format < time(7, 0):
        logging.info("Start Send message for one time schedule")
        utils = Utils()
        utils.email = os.getenv("NEWLXP_EMAIL", "")
        token = utils.get_token()
        
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
                await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Сегодня пар нет")
                return

            text = format_schedule_today_only(classes, today_str)
            
            await bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=text,
                parse_mode="HTML",
                disable_web_page_preview=True
            )

        except RuntimeError as e:
            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="❌ Ошибка сервера")
            logging.exception(f"Ошибка сервера {e}")
        except Exception as e:
            logging.exception(f"Ошибка в /today для группы {TELEGRAM_CHAT_ID}")
            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="❌ Не удалось получить расписание. Попробуйте позже.")