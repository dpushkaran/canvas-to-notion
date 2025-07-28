import os
import requests
from datetime import datetime
from models.assignment import Assignment

def fetch_assignments():
    token = os.getenv("CANVAS_API_TOKEN")
    courses_url = "https://canvas.unl.edu/api/v1/users/self/favorites/courses"
    assignments_url = "https://canvas.unl.edu/api/v1/courses/{course_id}/assignments"

    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})

    response = session.get(courses_url)
    if response.status_code != 200:
        raise Exception("Failed to fetch courses")

    assignments = []
    for course in response.json():
        course_id = course['id']
        course_name = course['name']
        response = session.get(assignments_url.format(course_id=course_id))

        if response.status_code != 200:
            continue

        for a in response.json():
            if a.get('due_at'):
                try:
                    due_date = datetime.fromisoformat(a['due_at'].replace("Z", "+00:00"))
                    assignments.append(Assignment(
                        name=a['name'],
                        due_date=due_date,
                        canvas_id=a['id'],
                        course_name=course_name,
                        url=a['html_url']
                    ))
                except Exception:
                    continue

    return assignments
