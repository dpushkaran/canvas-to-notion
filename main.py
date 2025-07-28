from utils.env_loader import *
from canvas.fetch_assignments import fetch_assignments
from notion.create_page import create_notion_page
from notion.check_duplicates import assignment_already_exists

def main():
    assignments = fetch_assignments()
    for assignment in assignments:
        if assignment_already_exists(assignment.canvas_id):
            print(f"Skipped (duplicate): {assignment.name}")
        else:
            create_notion_page(assignment)

if __name__ == "__main__":
    main()
