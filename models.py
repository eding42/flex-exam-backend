from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """
    Model which represents a user.
    """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String)

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    date_of_birth = db.Column(db.String)

    email = db.Column(db.String)
    testing_location = db.Column(db.String)
    reuse = db.Column(db.Boolean)
    testid = db.Column(db.String)

    examresponse = db.relationship("ExamResponse", uselist=False, back_populates="user")

class ExamResponse(db.Model):
    """
    Model which represents an exam response.
    Attached to a User.
    """
    __tablename__ = "response"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    testid = db.Column(db.String, db.ForeignKey("user.testid"))
    response = db.Column(db.Text)

    user = db.relationship("User", back_populates="response")
