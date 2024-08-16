from flask import abort, make_response

from config import db
from models import Accessment, Student, accessment_schema

def read_one(accessment_id):
    accessment = Accessment.query.get(accessment_id)

    if accessment is not None:
        return accessment_schema.dump(accessment)
    else:
        abort(
            404, f"Accessment with ID {accessment_id} not found"
        )
def update(accessment_id, accessment):
    existing_accessment = Accessment.query.get(accessment_id)

    if existing_accessment:
        update_accessment = accessment_schema.load(accessment, session=db.session)
        existing_accessment.acsmntDate = update_accessment.acsmntDate
        existing_accessment.acsr_fname = update_accessment.acsr_fname
        existing_accessment.acsr_lname = update_accessment.acsr_lname
        existing_accessment.acsr_staffID = update_accessment.acsr_staffID
        existing_accessment.acsr_phone = update_accessment.acsr_phone
        existing_accessment.acsr_email = update_accessment.acsr_email
        existing_accessment.comment = update_accessment.comment
        existing_accessment.timestamp = update_accessment.timestamp
        db.session.merge(existing_accessment)
        db.session.commit()
        return accessment_schema.dump(existing_accessment), 201
    else:
        abort(404, f"Note with ID {accessment_id} not found")

def delete(accessment_id):
    existing_accessment = Accessment.query.get(accessment_id)

    if existing_accessment:
        db.session.delete(existing_accessment)
        db.session.commit()
        return make_response(f"{accessment_id} successfully deleted", 204)
    else:
        abort(404, f"Accessment with ID {accessment_id} not found")

def create(accessment):
    student_id = accessment.get("student_id")
    student = Student.query.get(student_id)

    if student:
        new_accessment = accessment_schema.load(accessment, session=db.session)
        student.accessments.append(new_accessment)
        db.session.commit()
        return accessment_schema.dump(new_accessment), 201
    else:
        abort(
            404,
            f"Student not found for ID: {student_id}"
        )