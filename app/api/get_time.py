import requests
from config import TELEGRAM_CHAT_ID

TIMEAPI_URL = "https://timeapi.io/api/v1/time/current/zone?timezone=Asia/Novosibirsk"


async def get_current_time() -> str | None:
    """Возвращает значение ключа "time" из API или None при ошибке."""
    try:
        resp = requests.get(TIMEAPI_URL, timeout=10)
        resp.raise_for_status()
        return resp.json().get("time")
    except Exception:
        return None
