# Ryan Ott's DevMountain Capstone Project - Clock In/Clock Out Tracking App

Version 1.0

This clock in/clock out tracking app is designed for students to easily track their attendance and for administrators to manage the student clock data. The app is built on flask_sqlalchemy.

## How to create users

1. Start Database
2. In terminal:

```
Python3 -i model.py
```

<br>

```
>>> db.create_all()
```
<br>
3. To create a student user:

```
>>> new_student = Student(student_id='', first_name='', last_name='')
>>> db.session.add(new_student)
>>> db.session.commit()
```
<br>
4. To create an admin user:

```
>>> new_admin = Admin(login='', password='')
>>> db.session.add(new_admin)
>>> db.session.commit()
```


## Using the app

### As a student

1. On the homepage, enter your student ID.
2. If the student ID is valid, it will take you to the clock in/clock out page.
3. You can either clock in if your clock status is false or clock out if your clock status is true.
4. All clock events will be logged in a Clocks class that the student can view by hitting the "view all clocks" button.

### As an administrator

1. on the homepage, type "admin" into the field to access the admin login screen.
2. On the admin login screen, enter your admin login and password.
3. You will see a list of all the students with a details button for each list item.
4. Click the details button to access a page that shows all the student clock data and allows you to delete clock data.

## Known Issues

1. Back buttons need to be added to most pages.
2. If you delete a if a student is clocked in and you delete their clock entry before they clockout it will break their account.
