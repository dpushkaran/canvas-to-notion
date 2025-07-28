from dataclasses import dataclass
from datetime import datetime

@dataclass
class Assignment:
    name: str
    due_date: datetime
    canvas_id: int
    course_name: str
    url: str
