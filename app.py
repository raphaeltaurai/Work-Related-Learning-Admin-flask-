from flask import render_template, request, redirect, url_for
import config
from models import Student, Scheduling
from students import read_all, create, read_one, update, delete
import scheduler  # Import the scheduler module to start the scheduled tasks
import scheduler
from scheduling import create_schedule, read_schedules, read_one_schedule

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")


@app.route("/")
def home():
    students = Student.query.all()
    return render_template("studentList.html", students=students)

@app.route("/scheduling.html", methods=["GET", "POST"])
def scheduling():
    if request.method == "POST":
        scheduling_data = {
            "schdl_date": request.form.get("assessmentDate"),
            "schdle_city": request.form.get("assessmentCity"),
            "transport": request.form.get("assessmentTransport")
        }
        create_schedule(scheduling_data)
        return redirect(url_for('scheduling'))
    else:
        schedules = read_schedules()
        return render_template("scheduling.html", schedules=schedules)


@app.route("/student_info.html", methods=["GET", "POST"])
def student_info():
    if request.method == "POST":
        student_data = {
            "fname": request.form.get("fname"),
            "lname": request.form.get("lname"),
            "regNo": request.form.get("regNo"),
            "level": request.form.get("level"),
            "program": request.form.get("program"),
            "department": request.form.get("department"),
            "st_email": request.form.get("st_email"),
            "phoneNo": request.form.get("phoneNo"),
            "DOE": request.form.get("DOE"),
            "company": request.form.get("company"),
            "com_city": request.form.get("com_city"),
            "com_email": request.form.get("com_email"),
            "com_phone": request.form.get("com_phone")
        }

        regNo = student_data["regNo"]
        existing_student = Student.query.filter(Student.regNo == regNo).one_or_none()

        if existing_student:
            # Update existing student
            update(regNo, student_data)
            response = update(regNo, student_data)[0]
        else:
            # Create new student
            response = create(student_data)[0]

        return response

    else:
        regNo = request.args.get("regNo")
        if regNo:
            student = read_one(regNo)
            return student
        else:
            return render_template("student_info.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
