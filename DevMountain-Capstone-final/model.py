from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Time

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    clock_status = db.Column(db.Boolean, default=False, nullable=False)

class Clock(db.Model):
    __tablename__ = "clocks"

    clock_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    time_in = db.Column(Time, nullable=False)
    time_out = db.Column(Time, nullable=True)

    def to_dict(self):
        return {'student_id': self.student_id,
                'time_in': self.time_in.strftime('%I:%M:%S %p'),
                'time_out': self.time_out.strftime('%I:%M:%S %p') if self.time_out else None}


class Admin(db.Model):
    __tablename__ = "admins"

    admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    login = db.Column(db.String, unique=True)
    password = db.Column(db.String)


def connect_to_db(flask_app, db_uri="postgresql:///clocks", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
