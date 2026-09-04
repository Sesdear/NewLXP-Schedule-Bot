# api/sign_in.py
from api.graphql_query import graphql_query
from config import API_URL
import logging


def sign_in(email: str, password: str):
    """
    Выполняет вход в NewLXP и возвращает (lxp_user_id, access_token)
    """
    query = """
    query SignIn($input: SignInInput!) {
      signIn(input: $input) {
        user {
          id
        }
        accessToken
      }
    }
    """

    variables = {
        "input": {
            "email": email.strip(),
            "password": password  # пароль не логируем!
        }
    }

    try:
        result = graphql_query(API_URL, query, variables)
    except Exception as e:
        logging.error(f"Ошибка запроса к GraphQL при signIn: {e}")
        raise RuntimeError("Не удалось соединиться с сервером NewLXP")

    data = result.get("data")
    errors = result.get("errors")

    if errors:
        msg = errors[0].get("message", "Unknown error")
        logging.warning(f"GraphQL error при signIn: {msg} (email: {email})")

        if any(code in msg for code in ["INVALID_CREDENTIALS", "Unauthorized", "invalid_credentials"]):
            raise ValueError("Неверный email или пароль")
        raise RuntimeError(msg)

    if not data or not data.get("signIn"):
        raise RuntimeError("Неожиданный ответ от сервера")

    sign_in_data = data["signIn"]
    access_token = sign_in_data.get("accessToken")
    user_id = sign_in_data["user"].get("id")

    if not access_token or not user_id:
        raise RuntimeError("Не получен accessToken или user.id")

    return user_id, access_token