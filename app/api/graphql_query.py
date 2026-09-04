import requests


def graphql_query(api_url: str, query: str, variables=None, token: str = None):
    headers = {
        "Content-Type": "application/json",
        "apollographql-client-name": "web"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.post(
        api_url,
        json={
            "query": query,
            "variables": variables or {}
        },
        headers=headers,
        timeout=15
    )

    response.raise_for_status()
    return response.json()