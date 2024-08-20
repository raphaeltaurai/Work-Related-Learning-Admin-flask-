from datetime import datetime
from marshmallow_sqlalchemy import fields
from config import db, ma

class Accessment(db.Model):
    __tablename__ = "accessments"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    acsmntDate = db.Column(db.Date, nullable=False)
    acsr_fname = db.Column(db.String)
    acsr_lname = db.Column(db.String)
    acsr_staffID = db.Column(db.String, unique=True)
    acsr_phone = db.Column(db.String, nullable=False)
    acsr_email = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class AccessmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Accessment
        load_instance = True
        sqla_session = db.session
        include_fk = True

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(32))
    lname = db.Column(db.String(32))
    regNo = db.Column(db.String(32), unique=True)
    DOE = db.Column(db.Date)
    st_email = db.Column(db.String(32), unique=True)
    phoneNo = db.Column(db.String(13), unique=True)
    level = db.Column(db.String(10), default="3.1") #defaulted to 3.1 which is the beginning of wrl/attachment
    department = db.Column(db.String(252))
    program = db.Column(db.String(252))
    company = db.Column(db.String(86))
    com_city = db.Column(db.String(32))
    com_email = db.Column(db.String)
    com_phone = db.Column(db.String(32))

    accessments = db.relationship(
        Accessment,
        backref="student",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Accessment.timestamp)"
    )

class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    accessments = fields.Nested(AccessmentSchema, many=True)

class Scheduling(db.Model):
    __tablename__ = "scheduling"
    id = db.Column(db.Integer, primary_key=True)
    schdl_date = db.Column(db.Date, nullable=False)
    schdle_city = db.Column(db.String(32), nullable=False)
    transport = db.Column(db.String(86), nullable=True)
    studentlist = db.Column(db.Text, nullable=True)  # This will store JSON serialized list of students

class SchedulingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Scheduling
        load_instance = True
        sqla_session = db.session


accessment_schema = AccessmentSchema()
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)
scheduling_schema = SchedulingSchema()
schedulings_schema = SchedulingSchema(many=True)
