from datetime import datetime, date
from config import app, db
from models import Student, Scheduling

SCHEDULING_DATA = [
    {
        "schdl_date": "2024-08-15",
        "schdle_city": "Gweru",
        "transport": "Bus",
        "studentlist": '["Student1"]',  # JSON serialized list
    },
]

with app.app_context():
    db.create_all()
    for data in SCHEDULING_DATA:
        new_schedule = Scheduling(
            schdl_date=datetime.strptime(data.get("schdl_date"), "%Y-%m-%d").date(),
            schdle_city=data.get("schdle_city"),
            transport=data.get("transport"),
            studentlist=data.get("studentlist")
        )
        db.session.add(new_schedule)

    db.session.commit()
    print("Scheduling table created successfully.")
    print("Sample scheduling data added to the database successfully.")