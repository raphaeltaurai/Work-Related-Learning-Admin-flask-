from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from config import db
from models import Student
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

def update_student_levels():
    with scheduler.app.app_context():
        students = Student.query.all()
        for student in students:
            doe = student.DOE
            if doe + timedelta(days=180) <= datetime.utcnow():  # 6 months
                if student.level == "3.1":
                    student.level = "3.2"
                    db.session.add(student)
        db.session.commit()

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_student_levels, trigger="interval", hours=1)  # Check hourly
scheduler.start()