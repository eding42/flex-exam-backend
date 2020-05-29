from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TestID(db.Model):
    """
    Model representing a test ID.
    Start time is an ISO datetime string.
    """
    __tablename__ = "testid"

    id = db.Column(db.Integer, primary_key=True)
    testid = db.Column(db.String(8))
    starttime = db.Column(db.String(32))
    endtime = db.Column(db.String(32))

class User(db.Model):
    """
    Model which represents a user.
    """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(36))

    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    date_of_birth = db.Column(db.String(64))

    email = db.Column(db.String(128))
    testing_location = db.Column(db.String(32))
    reuse = db.Column(db.Boolean)

    examresponse = db.relationship("ExamResponse", uselist=False, back_populates="user")
    testid_id = db.Column(db.Integer, db.ForeignKey("testid.id"))
    testid = db.relationship("TestID", backref="users")

class ExamResponse(db.Model):
    """
    Model which represents an exam response.
    Attached to a User.
    """
    __tablename__ = "response"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    response = db.Column(db.Text)

    user = db.relationship("User", back_populates="examresponse")
    testid_id = db.Column(db.Integer, db.ForeignKey("testid.id"))
    testid = db.relationship("TestID", backref="responses")
