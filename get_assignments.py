from dotenv import load_dotenv
import os
import requests

load_dotenv()
token = os.getenv("CANVAS_API_TOKEN")

courses_url = "https://canvas.unl.edu/api/v1/users/self/favorites/courses"
assignments_url = "https://canvas.unl.edu/api/v1/courses/{course_id}/assignments"

session = requests.Session()
session.headers.update({"Authorization": f"Bearer {token}"})

r = session.get(courses_url)

if r.status_code == 200:
    print("Request was successful!")
    courses = r.json()
    for course in courses:
        print(f"Course Name: {course['name']}, Course ID: {course['id']}")
        formatted_url = assignments_url.format(course_id=course['id'])
        r = session.get(formatted_url)

        print(f"Assignments for {course['name']}:")
        if r.status_code == 200:
            assignments = r.json()
            for assignment in assignments:
                print(f"- {assignment['name']} (ID: {assignment['id']})")