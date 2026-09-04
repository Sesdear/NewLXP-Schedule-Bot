from datetime import datetime, timedelta
import logging
from api.graphql_query import graphql_query
from config import API_URL

def get_schedule(token: str, date_from: str, date_to: str):
    query = """
    query ManyClassesForSchedule($input: ManyClassesInput!) {
      manyClasses(input: $input) {
        id
        from
        to
        name
        role
        isOnline
        meetingLink
        discipline {
          name
          code
        }
        learningGroup {
          name
        }
        classroom {
          name
          buildingArea {
            name
          }
        }
        teachers {
          user {
            firstName
            lastName
            middleName
          }
        }
      }
    }
    """
    variables = {
        "input": {
            "page": 1,
            "pageSize": 50,
            "filters": {
                "roles": ["STUDENT", "TEACHER", "STUDENT_PARENT"],
                "interval": {
                    "from": date_from,
                    "to": date_to
                }
            }
        }
    }
    result = graphql_query(API_URL, query, variables, token=token)
    
    data = result.get("data")
    if not data or "manyClasses" not in data:
        errors = result.get("errors", [])
        msg = errors[0]["message"] if errors else "Неизвестная ошибка"
        raise RuntimeError(f"Ошибка получения расписания: {msg}")
    
    return data["manyClasses"]



NOVOSIBIRSK_OFFSET = timedelta(hours=7)

def format_schedule_message(classes, start_date_str: str):
    try:
        start_date = datetime.fromisoformat(start_date_str.replace("Z", "+00:00"))
    except:
        start_date = datetime.utcnow()

    weekdays = {
        0: "Понедельник", 1: "Вторник", 2: "Среда",
        3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье"
    }

    months = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля",
        5: "мая", 6: "июня", 7: "июля", 8: "августа",
        9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }

    schedule_by_day = {}

    for cls in classes:
        try:
            dt_from_utc = datetime.fromisoformat(cls["from"].replace("Z", "+00:00"))
            dt_to_utc = datetime.fromisoformat(cls["to"].replace("Z", "+00:00"))

            dt_from = dt_from_utc + NOVOSIBIRSK_OFFSET
            dt_to = dt_to_utc + NOVOSIBIRSK_OFFSET

            day_key = dt_from.date().isoformat()

            if day_key not in schedule_by_day:
                schedule_by_day[day_key] = []

            teacher = "Не указан"
            if cls["teachers"]:
                t = cls["teachers"][0]["user"]
                teacher = " ".join(filter(None, [
                    t.get("lastName", ""),
                    (t.get("firstName", "")[:1] + ".") if t.get("firstName") else "",
                    (t.get("middleName", "")[:1] + ".") if t.get("middleName") else ""
                ]))

            room = "Онлайн" if cls["isOnline"] else cls["classroom"]["name"]

            lesson = (
                f"🕒 <b>{dt_from.strftime('%H:%M')}–{dt_to.strftime('%H:%M')}</b>\n"
                f"<b>{cls['discipline']['name']}</b>\n"
                f"👤 {teacher}   📍 {room}"
            )

            if cls["isOnline"] and cls.get("meetingLink"):
                lesson += f'\n🔗 <a href="{cls["meetingLink"]}">Подключиться</a>'

            schedule_by_day[day_key].append((dt_from, lesson))

        except Exception as e:
            logging.warning(f"Ошибка обработки занятия {cls.get('id')}: {e}")

    lines = ["<b>📚 Расписание на неделю</b>"]

    current_day = start_date.date()

    for i in range(7):
        day = current_day + timedelta(days=i)
        day_key = day.isoformat()

        lines.append(
            f"\n📅 <b>{weekdays[day.weekday()]} · {day.day} {months[day.month]}</b>"
        )

        if day_key in schedule_by_day:
            schedule_by_day[day_key].sort(key=lambda x: x[0])

            for _, lesson in schedule_by_day[day_key]:
                lines.append("")
                lines.append(lesson)
        else:
            lines.append("\n🌙 <i>Выходной</i>")

        if i != 6:
            lines.append("\n──────────────")

    return "\n".join(lines)


def format_schedule_today_only(classes, today_str: str):
    try:
        today = datetime.fromisoformat(today_str).date()
    except:
        today = (datetime.utcnow() + NOVOSIBIRSK_OFFSET).date()

    weekdays = {
        0: "Понедельник", 1: "Вторник", 2: "Среда",
        3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье"
    }

    months = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля",
        5: "мая", 6: "июня", 7: "июля", 8: "августа",
        9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }

    lines = [
        "<b>📚 Расписание на сегодня</b>",
        f"\n📅 <b>{weekdays[today.weekday()]} · {today.day} {months[today.month]}</b>"
    ]

    lessons = []

    for cls in classes:
        try:
            dt_from = datetime.fromisoformat(cls["from"].replace("Z", "+00:00")) + NOVOSIBIRSK_OFFSET
            if dt_from.date() != today:
                continue

            dt_to = datetime.fromisoformat(cls["to"].replace("Z", "+00:00")) + NOVOSIBIRSK_OFFSET

            teacher = "Не указан"
            if cls["teachers"]:
                t = cls["teachers"][0]["user"]
                teacher = " ".join(filter(None, [
                    t.get("lastName", ""),
                    (t.get("firstName", "")[:1] + ".") if t.get("firstName") else "",
                    (t.get("middleName", "")[:1] + ".") if t.get("middleName") else ""
                ]))

            room = "Онлайн" if cls["isOnline"] else cls["classroom"]["name"]

            lesson = (
                f"🕒 <b>{dt_from.strftime('%H:%M')}–{dt_to.strftime('%H:%M')}</b>\n"
                f"<b>{cls['discipline']['name']}</b>\n"
                f"👤 {teacher}   📍 {room}"
            )

            if cls["isOnline"] and cls.get("meetingLink"):
                lesson += f'\n🔗 <a href="{cls["meetingLink"]}">Подключиться</a>'

            lessons.append((dt_from, lesson))

        except Exception as e:
            logging.warning(f"Ошибка обработки занятия: {e}")

    if not lessons:
        lines.append("\n🌙 <i>Сегодня выходной</i>")
        return "\n".join(lines)

    lessons.sort(key=lambda x: x[0])

    for _, lesson in lessons:
        lines.append("")
        lines.append(lesson)

    return "\n".join(lines)