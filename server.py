from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
from datetime import datetime, timedelta
import crud

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    return render_template('homepage.html')

#students


@app.route('/login', methods=['POST'])
def process_student_login():
    student_id = request.form['student_id']
    
    if student_id == 'admin':
        return render_template('/admin_login.html')
    
    if not student_id.isdigit():
        flash('Invalid student ID. Please try again.')
        return redirect('/')
    
    student = crud.get_student_by_id(student_id)
    if not student:
        flash('Invalid student ID. Please try again.')
        return redirect('/')

    session['student_id'] = student.student_id
    session['student_name'] = student.first_name
    flash(f"Welcome back,{student.first_name} {student.last_name}!")
    return redirect('/clock_screen.html')


@app.route('/clock_screen.html')
def clock_screen():
    student_id = session.get('student_id')
    student = crud.get_student_by_id(student_id)
    clock_data = crud.get_student_clock_data(student_id)
    return render_template('clock_screen.html', student=student, clock_data=clock_data)

@app.route("/clock_in", methods=["POST"])
def clock_in():
    student_id = session.get('student_id')
    crud.clock_in(student_id)
    flash("You have successfully clocked in!")
    return redirect('/clock_screen.html')

@app.route("/clock_out", methods=["POST"])
def clock_out():
    student_id = session.get('student_id')
    crud.clock_out(student_id)
    flash("You have successfully clocked out!")
    return redirect('/clock_screen.html')

@app.route("/clocks", methods=["GET"])
def all_clocks():
    student_id = session.get('student_id')
    student = crud.get_student_by_id(student_id)
    clock_data = crud.get_student_clock_data(student_id)
    return render_template('clocks.html', student=student, clock_data=clock_data)

#admins

@app.route("/admin_login", methods=["POST"])
def process_admin_login():
    login = request.form['login']
    password = request.form['password']
    admin = crud.get_admin_by_login(login)

    if admin.password != password:
        return flash("Incorrect login or password")
    else:
        students = crud.get_all_students()
        session['admin_id'] = admin.admin_id
        flash(f"Welcome back,{admin.login}!")
        return render_template('/admin_screen.html', students=students)

@app.route('/admin_screen')
def admin_screen():
    students = crud.get_all_students()
    return render_template('/admin_screen.html', students=students)

@app.route('/logout_admin', methods=['POST'])
def logout_admin():
    session.pop('admin_id', None)
    return render_template('/admin_login.html')

@app.route("/student_details/<student_id>")
def student_details(student_id):
    session['student_details_index'] = student_id
    student = crud.get_student_by_id(student_id)
    clock_data = crud.get_student_clock_data(student_id)
    return render_template("student_details.html", student=student, clock_data=clock_data)

@app.route('/back_from_student_details')
def back_from_student_details():
    session.pop('student_details_index', None)
    return redirect('/admin_screen')

@app.route('/delete_clock_entry/<clock_id>', methods=['POST'])
def delete_clock_entry(clock_id):
    student_id = session['student_details_index']
    clock = crud.get_clock_by_clock_id(clock_id)
    last_clock = crud.get_student_last_clock(student_id)
    if last_clock.clock_id == (clock_id) and last_clock.time_out is None:
        flash('Cannot delete clock entry: student has not clocked out yet')
    else:
        db.session.delete(clock)
        db.session.commit()

    return redirect(f'/student_details/{student_id}')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', port=5006, debug=True)
