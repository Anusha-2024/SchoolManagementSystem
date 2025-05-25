from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yourpassword',
    'database': 'db'
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # For demonstration, use hardcoded username and password
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/students')
@login_required
def students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT student_id, first_name, last_name, date_of_birth, gender, email, enrollment_date, class_id FROM Student")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('students.html', students=students)

@app.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        email = request.form['email']
        enrollment_date = request.form['enrollment_date']
        class_id = request.form['class_id']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Student (first_name, last_name, date_of_birth, gender, email, enrollment_date, class_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, date_of_birth, gender, email, enrollment_date, class_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('students'))
    return render_template('students_add.html')

@app.route('/classes')
@login_required
def classes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Class")
    classes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('classes.html', classes=classes)

@app.route('/classes/add', methods=['GET', 'POST'])
@login_required
def add_class():
    if request.method == 'POST':
        class_name = request.form['class_name']
        section = request.form['section']
        year = request.form['year']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Class (class_name, section, year)
            VALUES (%s, %s, %s)
        """, (class_name, section, year))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('classes'))
    return render_template('classes_add.html')

@app.route('/teachers')
@login_required
def teachers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Teacher")
    teachers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('teachers.html', teachers=teachers)

@app.route('/teachers/add', methods=['GET', 'POST'])
@login_required
def add_teacher():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        contact_number = request.form['contact_number']
        email = request.form['email']
        hire_date = request.form['hire_date']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Teacher (first_name, last_name, date_of_birth, gender, contact_number, email, hire_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, date_of_birth, gender, contact_number, email, hire_date))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('teachers'))
    return render_template('teachers_add.html')

@app.route('/attendance')
@login_required
def attendance():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Attendance")
    attendance_records = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('attendance.html', attendance=attendance_records)

@app.route('/attendance/add', methods=['GET', 'POST'])
@login_required
def add_attendance():
    if request.method == 'POST':
        student_id = request.form['student_id']
        class_id = request.form['class_id']
        attendance_date = request.form['attendance_date']
        status = request.form['status']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Attendance (student_id, class_id, attendance_date, status)
            VALUES (%s, %s, %s, %s)
        """, (student_id, class_id, attendance_date, status))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('attendance'))
    return render_template('attendance_add.html')

@app.route('/complaints')
@login_required
def complaints():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.complaint_id, c.student_id, i.issue_description AS issue, c.complaint_date, s.status_name AS status
        FROM Complaint c
        JOIN Issue i ON c.issue_id = i.issue_id
        JOIN Status s ON c.status_id = s.status_id
    """)
    complaints = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('complaints.html', complaints=complaints)
@app.route('/complaints/add', methods=['GET', 'POST'])
@login_required
def add_complaint():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        issue_id = request.form['issue_id']
        complaint_date = request.form['complaint_date']
        status_id = request.form['status_id']

        cursor.execute("""
            INSERT INTO Complaint (student_id, issue_id, complaint_date, status_id)
            VALUES (%s, %s, %s, %s)
        """, (student_id, issue_id, complaint_date, status_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('complaints'))
    
    # GET method: fetch issues and statuses for dropdown
    cursor.execute("SELECT * FROM Issue")
    issues = cursor.fetchall()

    cursor.execute("SELECT * FROM Status")
    statuses = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('complaints_add.html', issues=issues, statuses=statuses)
@app.route('/events')
@login_required
def events():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Event")
    events = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('events.html', events=events)

@app.route('/events/add', methods=['GET', 'POST'])
@login_required
def add_event():
    if request.method == 'POST':
        info_id = request.form['info_id']
        event_date = request.form['event_date']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Event (info_id, event_date)
            VALUES (%s, %s)
        """, (info_id, event_date))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('events'))
    return render_template('events_add.html')

@app.route('/extracurricular_activities')
@login_required
def extracurricular_activities():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Extracurricular_Activity")
    activities = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('extracurricular_activities.html', activities=activities)

@app.route('/extracurricular_activities/add', methods=['GET', 'POST'])
@login_required
def add_extracurricular_activity():
    if request.method == 'POST':
        activity_name = request.form['activity_name']
        description = request.form['description']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Extracurricular_Activity (activity_name, description)
            VALUES (%s, %s)
        """, (activity_name, description))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('extracurricular_activities'))
    return render_template('extracurricular_activities_add.html')

@app.route('/fee_payments')
@login_required
def fee_payments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Fee_Payment")
    payments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('fee_payments.html', payments=payments)

@app.route('/fee_payments/add', methods=['GET', 'POST'])
@login_required
def add_fee_payment():
    if request.method == 'POST':
        student_id = request.form['student_id']
        amount = request.form['amount']
        payment_date = request.form['payment_date']
        payment_method = request.form['payment_method']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Fee_Payment (student_id, amount, payment_date, payment_method)
            VALUES (%s, %s, %s, %s)
        """, (student_id, amount, payment_date, payment_method))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('fee_payments'))
    return render_template('fee_payments_add.html')

@app.route('/feedbacks')
@login_required
def feedbacks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Feedback")
    feedbacks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('feedbacks.html', feedbacks=feedbacks)

@app.route('/feedbacks/add', methods=['GET', 'POST'])
@login_required
def add_feedback():
    if request.method == 'POST':
        student_id = request.form['student_id']
        feedback_text = request.form['feedback_text']
        feedback_date = request.form['feedback_date']
        feedback_type = request.form['feedback_type']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Feedback (student_id, feedback_text, feedback_date, type)
            VALUES (%s, %s, %s, %s)
        """, (student_id, feedback_text, feedback_date, feedback_type))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('feedbacks'))
    return render_template('feedbacks_add.html')

@app.route('/holidays')
@login_required
def holidays():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Holiday")
    holidays = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('holiday.html', holidays=holidays)

@app.route('/holidays/add', methods=['GET', 'POST'])
@login_required
def add_holiday():
    if request.method == 'POST':
        name = request.form['holiday_name']
        date = request.form['holiday_date']
        description = request.form['description']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Holiday (holiday_name, holiday_date, description)
            VALUES (%s, %s, %s)
        """, (name, date, description))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('holidays'))

    return render_template('add_holiday.html')

@app.route('/marks')
@login_required
def marks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Mark ORDER BY student_id DESC")
    marks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('marks.html', marks=marks)

@app.route('/marks/add', methods=['GET', 'POST'])
@login_required
def add_mark():
    if request.method == 'POST':
        mark_id = request.form['mark_id']
        student_id = request.form['student_id']
        subject_id = request.form['subject_id']
        exam_type = request.form['exam_type']
        score = request.form['score']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO MARK (mark_id, student_id, subject_id, exam_type, score)
            VALUES (%s, %s, %s, %s, %s)
        """, (mark_id, student_id, subject_id, exam_type, score))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('marks'))

    return render_template('add_mark.html')

@app.route('/student_events')
@login_required
def student_events():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Student_Event")
    student_events = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('student_events.html', student_events=student_events)

@app.route('/add_student_event', methods=['GET', 'POST'])
@login_required
def add_student_event():
    if request.method == 'POST':
        student_id = request.form['student_id']
        event_id = request.form['event_id']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Student_Event (student_id, event_id) VALUES (%s, %s)", (student_id, event_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('student_events'))

    return render_template('add_student_event.html')

@app.route('/student_extracurricular')
@login_required
def student_extracurricular():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Student_Extracurricular")
    student_extracurricular = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('student_extracurricular.html', student_extracurricular=student_extracurricular)

@app.route('/student_transport')
@login_required
def student_transport():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Student_Transport")
    student_transport = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('student_transport.html', student_transport=student_transport)

@app.route('/transports')
@login_required
def transports():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Transport")
    transports = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('transports.html', transports=transports)

@app.route('/logout')
def logout():
    session.clear()  # Ends the user session
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
