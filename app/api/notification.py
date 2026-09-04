from api.graphql_query import graphql_query
from config import API_URL
from datetime import datetime, timedelta
import logging

def get_notifications(token: str):
    query = """
    query GetNotifications($input: NotificationsInput!) {
      notifications(input: $input) {
        items {
          id
          title
          body
          createdAt
          isRead
          __typename
        }
        hasMore
        total
        __typename
      }
    }
    """
    variables = {
        "input": {
            "filters": {},
            "page": 1,
            "pageSize": 20
        }
    }
    result = graphql_query(API_URL, query, variables, token=token)
    data = result.get("data", {}).get("notifications", {})
    return data.get("items", [])

NOVOSIBIRSK_OFFSET = timedelta(hours=7)

import re

def clean_html_for_telegram(body: str) -> str:

    body = re.sub(r'<p[^>]*>', '', body)
    body = re.sub(r'</p>', '\n', body)

    body = re.sub(r'<ol[^>]*>', '\n', body)
    body = re.sub(r'</ol>', '\n', body)

    body = re.sub(r'<ul[^>]*>', '\n', body)
    body = re.sub(r'</ul>', '\n', body)

    body = re.sub(r'<li[^>]*>', '• ', body)
    body = re.sub(r'</li>', '\n', body)

    body = re.sub(r'<[^<]+?>', '', body)

    body = re.sub(r'\n{3,}', '\n\n', body.strip())

    return body

def format_notification(item):
    dt = datetime.fromisoformat(item["createdAt"].replace("Z", "+00:00")) + NOVOSIBIRSK_OFFSET
    time_str = dt.strftime("%H:%M %d.%m.%Y")

    title = item["title"]

    body = clean_html_for_telegram(item["body"])

    return f"🔔 <b>{title}</b>\n{body}\n\n<i>{time_str}</i>"

def mark_notifications_as_read(token: str, notification_ids: list[str]):
    """
    Отмечает список уведомлений как прочитанные.
    notification_ids — список строковых ID
    """
    if not notification_ids:
        return

    query = """
    mutation MarkNotificationsAsRead($input: MarkNotificationsAsReadInput!) {
      markNotificationsAsRead(input: $input)
    }
    """

    variables = {
        "input": {
            "notificationsIds": notification_ids
        }
    }

    try:
        result = graphql_query(API_URL, query, variables, token=token)

        return result.get("data", {}).get("markNotificationsAsRead") is not None
    except Exception as e:
        logging.warning(f"Ошибка при отметке уведомлений как прочитанных: {e}")
        return False