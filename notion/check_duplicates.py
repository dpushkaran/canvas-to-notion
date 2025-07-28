import os
import requests

def assignment_already_exists(canvas_id: int) -> bool:
    token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")
    url = f"https://api.notion.com/v1/databases/{database_id}/query"

    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    body = {
        "filter": {
            "property": "ID",
            "number": {
                "equals": canvas_id
            }
        }
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code != 200:
        return False

    data = response.json()
    return len(data.get("results", [])) > 0
