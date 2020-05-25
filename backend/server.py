import uuid
import flask
from flask import request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import flask_sqlalchemy as SQLAlchemy
from backend.models import db, TestID, User, ExamResponse
from backend.admin_views import FlexModelView

# Init flask and SQLAlchemy
DB_URL = "localhost:3066"
DB_USER = "flexexam"
DB_PASSWORD = "xXFlex69Xx"
DB_NAME = "flexexam"

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}"
app.secret_key = "super secret"
db.init_app(app)

# Init admin interface
admin = Admin(app, name='flex-exam-backend', template_mode='bootstrap3')
admin.add_view(FlexModelView(TestID, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(ExamResponse, db.session))

@app.route("/")
def index():
    """
    Return a generic 200 SUCCESS message.
    """
    return "Success!"

@app.route("/api/<testid>", methods=["POST"])
def testid_register(testid):
    """
    Given the user's personal info, return a token representing the user.
    This token should be stored in a session cookie on the frontend side.
    """
    form = request.form

    # Create the user and add data
    testid = TestID.query.filter_by(testid=testid).first()
    if not testid:
        return "Test ID Not Found", 400

    try:
        user = User()
        user.token = str(uuid.uuid4())
        user.testid = testid
        user.reuse = False
        user.first_name = form["firstname"]
        user.last_name = form["firstname"]
        user.email = form["email"]
        user.date_of_birth = form["dateofbirth"]
        user.testing_location = form["testinglocation"]

        db.session.add(user)
        db.session.commit()
    except KeyError as e:
        print(form)
        print(e)
        return "Missing field", 400

    # Send back le token
    return user.token

@app.route("/api/<testid>/submit_exam", methods=["POST"])
def submit_exam(testid):
    """
    Submit an exam.
    This method authenticates against the user token
    and records the exam.
    """
    form = request.form

    if "token" not in form.keys():
        return "No token specified", 400
    if "response" not in form.keys():
        return "Response field empty", 400

    # Authenticate against the user (simple for now)
    # Possibly unsafe, not sure yet, need to test/research
    user = User.query.filter_by(token=form["token"]).first()
    if not user:
        return "Token invalid", 403
    elif user.reuse:
        return "User already submitted", 403
    else:
        user.reuse = True

        exam = ExamResponse()
        exam.user = user
        exam.response = form["response"]

        db.session.add(exam)
        db.session.add(user)
        db.session.commit()
        return "Success"

if __name__ == "__main__":
    app.run(port=8000)
