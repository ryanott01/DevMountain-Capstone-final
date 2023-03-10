from model import db, Student, Admin, Clock, connect_to_db
from datetime import datetime


#students

def get_all_clock_data():
    clock_data = Clock.query.all()
    return clock_data

def get_student_by_id(id_number):
    return Student.query.get(id_number)

def get_all_students():
    return Student.query.all()

def get_student_clock_data(student_id):
    return Clock.query.filter_by(student_id=student_id).all()

def clock_in(student_id):
    clock_in_time = datetime.now().time()
    new_clock = Clock(student_id=student_id, date=datetime.now().date(), time_in=clock_in_time)

    student = get_student_by_id(student_id)
    student.clock_status = True
    db.session.add(new_clock)
    db.session.commit()

def clock_out(student_id):
    clock_out_time = datetime.now().time()

    latest_clock_in = Clock.query.filter_by(student_id=student_id, time_out=None).order_by(Clock.time_in.desc()).first()
    latest_clock_in.time_out = clock_out_time

    student = get_student_by_id(student_id)
    student.clock_status = False
    db.session.commit()

def get_student_last_clock(student_id):
    return Clock.query.filter_by(student_id=student_id).order_by(Clock.time_in.desc()).first()

def get_student_clock_status(student_id):
    last_clock = get_student_last_clock(student_id)
    if last_clock is None:
        return False
    elif last_clock.time_out is None:
        return True
    else:
        return False
    
#admins

def get_admin_by_login(login):
    return Admin.query.filter_by(login=login).first()

def get_clock_by_clock_id(clock_id):
    return Clock.query.get(clock_id)

def delete_clock_entry(clock_id):
    clock = Clock.query.get(clock_id)
    if clock:
        db.session.delete(clock)
        db.session.commit()
   
