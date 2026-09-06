import os, logging
from database import Utils
from api.sign_in import sign_in


async def token_refresh():
    """
    Обновляет токен авторизации каждые 20 минут через повторный вход в систему.
    """
    email = os.getenv("NEWLXP_EMAIL", "")
    password = os.getenv("NEWLXP_PASSWORD", "")

    if not email or not password:
        logging.error("Bot not configured for token refresh")
        return

    try:
        user_id, new_token = sign_in(email=email, password=password)
    except ValueError as e:
        logging.error("Token refresh failed - invalid credentials: %s", e)
        return
    except RuntimeError as e:
        logging.error("Token refresh failed - server error: %s", e)
        return

    utils = Utils()
    utils.email = email
    utils.set_token(user_id=user_id, new_token=new_token)

    logging.info("Token refreshed successfully for user %s", user_id)