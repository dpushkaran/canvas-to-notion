from dotenv import load_dotenv
import os
import requests

load_dotenv()
token = os.getenv("CANVAS_API_TOKEN")

requests_url = "https://canvas.unl.edu/api/v1/users/self/favorites/courses"

session = requests.Session()
session.headers.update({"Authorization": f"Bearer {token}"})

r = session.get(requests_url)

if r.status_code == 200:
    print("Request was successful!")
    courses = r.json()
    for course in courses:
        print(f"Course Name: {course['name']}, Course ID: {course['id']}")