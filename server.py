import flask
import uuid
from flask import request
import flask_sqlalchemy as SQLAlchemy
from models import db, User, ExamResponse

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://localhost:3066"
db.init_app(app)

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

    # Create the user and add data
    try:
        user = User()
        user.token = str(uuid.uuid4())
        user.testid = testid
        user.first_name = form["firstname"]
        user.last_name = form["firstname"]
        user.email = form["email"]
        user.date_of_birth = form["dateofbirth"]
        user.testing_location = form["testinglocation"]

        db.session.add(user)
        db.session.commit()
    except KeyError:
        return "Missing field", 400

    # Send back le token
    return user.token

@app.route("/api/<testid>/submit_exam", methods=["POST"])
def submit_exam():
    """
    Submit an exam.
    This method authenticates against the user token
    and records the exam.
    """
    if "token" not in form.keys():
        return "No token specified", 400
    if "response" not in form.keys():
        return "Response field empty", 400

    # Authenticate against the user (simple for now)
    # Possibly unsafe, not sure yet, need to test/research
    user = User.query.filter_by(token=form["token"])
    if not user:
        return "Token invalid", 403
    else:
        exam = ExamResponse()
        exam.user = user
        exam.response = form["response"]

        db.session.add(exam)
        db.session.commit()

if __name__ == "__main__":
    app.run(port=8000)
