import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import os

from config import TELEGRAM_TOKEN
from handlers import *
from api.token_refresh import token_refresh
from api.sign_in import sign_in
from database import Utils, Newlxp, engine
from sqlalchemy.orm import Session

async def per_hour( ):
    while True:
        await asyncio.sleep(60)
        logging.info("Token updater start")
        await token_refresh()

async def auth():
    logging.info("Start startup auth")

    email = os.getenv("NEWLXP_EMAIL", "")
    password = os.getenv("NEWLXP_PASSWORD", "")

    if not email or not password:
        logging.error("Bot not configured")
        return

    try:
        user_id, token = sign_in(
            email=email,
            password=password
        )
    except ValueError as e:
        logging.error("Authentication failed: %s", e)
        return
    except RuntimeError as e:
        logging.error("Error in sign_in: %s", e)
        return

    utils = Utils()
    utils.email = email
    utils.set_token(
        user_id=user_id,
        new_token=token
    )

    logging.info("Successfully authenticated user %s", user_id)
    
async def main():
    if not os.getenv("TELEGRAM_TOKEN") or not os.getenv("TELEGRAM_CHAT_ID") or not os.getenv("NEWLXP_EMAIL") or not os.getenv("NEWLXP_PASSWORD"):
        logging.error("Env variables can't be nullable")
    
    logging.basicConfig(level=logging.INFO)
    
    await auth()
    
    
    
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(today_router)
    dp.include_router(start_router)
    dp.include_router(tomorrow_router)
    dp.include_router(schedule_router)
    
    asyncio.create_task(per_hour())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
