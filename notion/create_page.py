import os
import requests
from models.assignment import Assignment

def create_notion_page(assignment: Assignment):
    notion_token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")
    url = "https://api.notion.com/v1/pages"

    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    body = {
        "parent": { "database_id": database_id },
        "properties": {
            "Name": {
                "title": [{"text": {"content": assignment.name}}]
            },
            "Due Date": {
                "date": { "start": assignment.due_date.isoformat() }
            },
            "ID": {
                "number": assignment.canvas_id
            },
            "Course": {
                "rich_text": [{"text": {"content": assignment.course_name}}]
            },
            "URL": {
                "url": assignment.url
            }
        }
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        print(f"Created in Notion: {assignment.name}")
    else:
        print(f"Failed: {assignment.name} | {response.status_code} | {response.text}")
