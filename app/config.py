from os import getenv
import logging

API_URL = "https://api.newlxp.ru/graphql"
try:
    TELEGRAM_TOKEN: str = getenv("TELEGRAM_TOKEN", "")
    TELEGRAM_CHAT_ID: int = int(getenv("TELEGRAM_CHAT_ID", 0))
except Exception as e:
    logging.error(f"Chat id key in env not int:\n\n{e}")