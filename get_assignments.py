from dotenv import load_dotenv
import os
import requests
from datetime import datetime


def create_notion_page(assignment_name, due_date):
    notion_token = os.getenv("NOTION_TOKEN")
    notion_database_id = os.getenv("NOTION_DATABASE_ID")
    notion_url = "https://api.notion.com/v1/pages"

    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    body = {
        "parent": {
            "database_id": notion_database_id
        },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": assignment_name
                        }
                    }
                ]
            },
            "Due Date": {
                "date": {
                    "start": due_date.isoformat()
                }
            }
        }
    }

    response = requests.post(notion_url, headers=headers, json=body)

    if response.status_code == 200:
        print(f"✅ Added to Notion: {assignment_name}")
    else:
        print(f"❌ Failed to add '{assignment_name}' | Status: {response.status_code} | Message: {response.text}")



load_dotenv()
token = os.getenv("CANVAS_API_TOKEN")

courses_url = "https://canvas.unl.edu/api/v1/users/self/favorites/courses"
assignments_url = "https://canvas.unl.edu/api/v1/courses/{course_id}/assignments"

date_format = "%A, %B %-d at %-I:%M %p, %Y"


canvas_session = requests.Session()
canvas_session.headers.update({"Authorization": f"Bearer {token}"})

r = canvas_session.get(courses_url)

if r.status_code == 200:
    print("Request was successful!")
    courses = r.json()
    for course in courses:
        print(f"Course Name: {course['name']}, Course ID: {course['id']}")
        formatted_url = assignments_url.format(course_id=course['id'])
        r = canvas_session.get(formatted_url)

        #print(f"Assignments for {course['name']}:")
        if r.status_code == 200:
            assignments = r.json()
            for assignment in assignments:
                if assignment['due_at'] != None:
                    due_date = datetime.fromisoformat(assignment['due_at'])
                    #print(f"- {assignment['name']} (ID: {assignment['id']}) due at {due_date.strftime(date_format)}")
                
                #print(f"- {assignment['name']} (ID: {assignment['id']})")
                    create_notion_page(assignment['name'], due_date)