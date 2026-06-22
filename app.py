from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

INDIAN_STATES = [
    "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar",
    "Chhattisgarh","Goa","Gujarat","Haryana",
    "Himachal Pradesh","Jharkhand","Karnataka","Kerala",
    "Madhya Pradesh","Maharashtra","Manipur","Meghalaya",
    "Mizoram","Nagaland","Odisha","Punjab",
    "Rajasthan","Sikkim","Tamil Nadu","Telangana",
    "Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
    "Andaman and Nicobar Islands","Chandigarh",
    "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi","Jammu and Kashmir","Ladakh",
    "Lakshadweep","Puducherry"
]

def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        number TEXT,
        email TEXT,
        course TEXT,
        state TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students ORDER BY id")
    students = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        students=students,
        states=INDIAN_STATES
    )

@app.route('/add', methods=['POST'])
def add_student():

    name = request.form['name']
    number = request.form['number']
    email = request.form['email']
    course = request.form['course']
    state = request.form['state']

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (name,number,email,course,state)
    VALUES(?,?,?,?,?)
    """, (name,number,email,course,state))

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete_student(id):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()

    cursor.execute("""
    SELECT name,number,email,course,state
    FROM students
    ORDER BY id
    """)

    data = cursor.fetchall()

    cursor.execute("DELETE FROM students")

    new_id = 1

    for row in data:
        cursor.execute("""
        INSERT INTO students
        (id,name,number,email,course,state)
        VALUES(?,?,?,?,?,?)
        """, (
            new_id,
            row[0],
            row[1],
            row[2],
            row[3],
            row[4]
        ))
        new_id += 1

    conn.commit()

    cursor.execute("""
    DELETE FROM sqlite_sequence
    WHERE name='students'
    """)

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/edit/<int:id>')
def edit_student(id):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        student=student,
        states=INDIAN_STATES
    )

@app.route('/update/<int:id>', methods=['POST'])
def update_student(id):

    name = request.form['name']
    number = request.form['number']
    email = request.form['email']
    course = request.form['course']
    state = request.form['state']

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE students
    SET
        name=?,
        number=?,
        email=?,
        course=?,
        state=?
    WHERE id=?
    """, (
        name,
        number,
        email,
        course,
        state,
        id
    ))

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == "__main__":
    app.run()
