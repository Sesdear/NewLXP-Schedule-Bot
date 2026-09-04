# api/profile.py
from api.graphql_query import graphql_query
from config import API_URL

def get_user_profile(token: str, lxp_user_id: str):
    query = """
    query GetUserById($input: GetUserByIdInput!) {
      getUserById(input: $input) {
        firstName
        lastName
        middleName
        email
        phoneNumber
        roles
        assignedGroups_v2 {
          learningGroup {
            name
            __typename
          }
          __typename
        }
        assignedSpecialties {
          isDeactivated
          specialty {
            name
            __typename
          }
          roles
          __typename
        }
        student {
          mainFormsEducation {
            currentForm {
              form
              startedAt
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
    }
    """

    variables = {
        "input": {
            "userId": lxp_user_id
        }
    }

    result = graphql_query(API_URL, query, variables, token=token)
    
    data = result.get("data")
    if not data or not data.get("getUserById"):
        errors = result.get("errors", [])
        msg = errors[0]["message"] if errors else "Неизвестная ошибка"
        raise RuntimeError(f"Ошибка получения профиля: {msg}")

    return data["getUserById"]