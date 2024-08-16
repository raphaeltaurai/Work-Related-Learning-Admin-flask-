from datetime import datetime, date
from config import app, db
from models import Student, Accessment

STUDENTS_ACCESSMENTS = [
    {
        "fname": "Chikomo",
        "lname": "Chemari",
        "regNo": "R23SAMPLE",
        "DOE": "2024-08-09",
        "st_email": "r23sample@.com",
        "phoneNo": "+263700000000",
        "level": "3.1",
        "department": "Business Sciences",
        "program": "Data Science and Informatics",
        "company": "ZIMCARE",
        "com_city": "Gweru",
        "com_email": "zimcare@hr.com",
        "com_phone": "+263 0000000",
        "accessments": [
            ("2024-08-13", "Sample", "Anames", "STAFF123", "+263750000000", "Staffsample@.com", "Commited kid", "2024-08-13 09:15:03")
        ],
    },
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for data in STUDENTS_ACCESSMENTS:
        new_student = Student(
            fname=data.get("fname"),
            lname=data.get("lname"),
            regNo=data.get("regNo"),
            DOE=datetime.strptime(data.get("DOE"), "%Y-%m-%d").date(),  # Ensure DOE is a date object
            st_email=data.get("st_email"),
            phoneNo=data.get("phoneNo"),
            level=data.get("level"),
            department=data.get("department"),
            program=data.get("program"),
            company=data.get("company"),
            com_city=data.get("com_city"),
            com_email=data.get("com_email"),
            com_phone=data.get("com_phone")
        )
        for acsmntDate, acsr_fname, acsr_lname, acsr_staffID, acsr_phone, acsr_email, comment, timestamp in data.get("accessments", []):
            new_student.accessments.append(
                Accessment(
                    acsmntDate=datetime.strptime(acsmntDate, "%Y-%m-%d").date(),
                    acsr_fname=acsr_fname,
                    acsr_lname=acsr_lname,
                    acsr_staffID=acsr_staffID,
                    acsr_phone=acsr_phone,
                    acsr_email=acsr_email,
                    comment=comment,
                    timestamp=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
                )
            )
        db.session.add(new_student)
    db.session.commit()