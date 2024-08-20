from flask import abort, make_response
from config import db
from models import Scheduling, scheduling_schema, schedulings_schema, Student, students_schema

def create_schedule(scheduling_data):
    city = scheduling_data.get('schdle_city')
    students = Student.query.filter(Student.com_city == city).all()

    if not students:
        abort(404, f"No students found in city {city}")

    # Extract student details and format them with a newline after each student
    student_list = '\n'.join(
        f"{student.fname} {student.lname} {student.regNo} {student.program} {student.company} {student.com_phone};"
        for student in students
    )

    # Count the number of students and append it to the student list
    student_count = len(students)
    student_list += f"\n\nTotal Students: {student_count}"

    scheduling_data['studentlist'] = student_list  # No need to serialize as JSON

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

def delete_schedule(schedule_id):
    schedule = Scheduling.query.get(schedule_id)

    if schedule is not None:
        db.session.delete(schedule)
        db.session.commit()
        return make_response(f"Schedule {schedule_id} successfully deleted", 204)
    else:
        abort(404, f"Schedule with ID {schedule_id} not found")