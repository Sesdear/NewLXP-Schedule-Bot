from datetime import time
from api.notification import get_notifications
from database import Utils
import os, logging
from api.sign_in import sign_in
async def token_refresh():
    utils = Utils()
    utils.email = os.getenv("NEWLXP_EMAIL", "")
    token = utils.get_token()
    if not token:
        logging.error("Null auth token")
        return
    get_notifications(token)