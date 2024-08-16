from flask import render_template
import config
from models import Student
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

@app.route("/scheduling")
def scheduling():
    return render_template("scheduling.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
