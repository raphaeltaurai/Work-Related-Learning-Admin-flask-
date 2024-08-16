from flask import abort, make_response
import json
from config import db
from models import Scheduling, scheduling_schema, schedulings_schema, Student, students_schema

def create_schedule(scheduling_data):
    city = scheduling_data.get('schdle_city')
    students = Student.query.filter(Student.com_city == city).all()

    if not students:
        abort(404, f"No students found in city {city}")

    student_list = students_schema.dump(students)
    scheduling_data['studentlist'] = json.dumps(student_list)  # Serialize the list of students

    new_schedule = scheduling_schema.load(scheduling_data, session=db.session)
    db.session.add(new_schedule)
    db.session.commit()

    return scheduling_schema.dump(new_schedule), 201

def read_schedules():
    schedules = Scheduling.query.all()
    return schedulings_schema.dump(schedules)

def read_one_schedule(schedule_id):
    schedule = Scheduling.query.get(schedule_id)

    if schedule is not None:
        return scheduling_schema.dump(schedule)
    else:
        abort(404, f"Schedule with ID {schedule_id} not found")