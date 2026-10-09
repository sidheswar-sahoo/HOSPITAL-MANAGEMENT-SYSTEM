from functools import wraps
from datetime import date

from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error

from config import Config

app = Flask(__name__)
app.config.from_object(Config)


def get_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DATABASE'],
    )


def fetch_all(query, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def fetch_one(query, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def execute_query(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    conn.commit()
    cursor.close()
    conn.close()


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please login first.', 'warning')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped_view


@app.route('/')
def home():
    if 'admin_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please enter username and password.', 'danger')
            return render_template('login.html')

        try:
            admin = fetch_one('SELECT * FROM admin WHERE username = %s', (username,))
            if admin and admin['password'] == password:
                session['admin_id'] = admin['id']
                session['username'] = admin['username']
                flash('Login successful.', 'success')
                return redirect(url_for('dashboard'))
            flash('Invalid username or password.', 'danger')
        except Error as e:
            flash(f'Database error: {e}', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'patients': fetch_one('SELECT COUNT(*) AS count FROM patients')['count'],
        'doctors': fetch_one('SELECT COUNT(*) AS count FROM doctors')['count'],
        'appointments': fetch_one('SELECT COUNT(*) AS count FROM appointments')['count'],
        'scheduled': fetch_one("SELECT COUNT(*) AS count FROM appointments WHERE status = 'Scheduled'")['count'],
    }
    today_appointments = fetch_one('SELECT COUNT(*) AS count FROM appointments WHERE appointment_date = %s', (date.today(),))['count']
    return render_template('dashboard.html', stats=stats, today_appointments=today_appointments)


@app.route('/patients')
@login_required
def patients():
    search = request.args.get('search', '').strip()
    if search:
        patients_list = fetch_all(
            '''SELECT * FROM patients
               WHERE CAST(patient_id AS CHAR) LIKE %s OR name LIKE %s
               ORDER BY patient_id DESC''',
            (f'%{search}%', f'%{search}%')
        )
    else:
        patients_list = fetch_all('SELECT * FROM patients ORDER BY patient_id DESC')
    return render_template('patients.html', patients=patients_list, search=search)


@app.route('/patients/add', methods=['GET', 'POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        gender = request.form.get('gender', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        disease = request.form.get('disease', '').strip()

        if not all([name, age, gender, phone, address, disease]):
            flash('All fields are required.', 'danger')
            return render_template('add_patient.html')

        execute_query(
            'INSERT INTO patients (name, age, gender, phone, address, disease) VALUES (%s, %s, %s, %s, %s, %s)',
            (name, age, gender, phone, address, disease)
        )
        flash('Patient added successfully.', 'success')
        return redirect(url_for('patients'))

    return render_template('add_patient.html')


@app.route('/patients/edit/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def edit_patient(patient_id):
    patient = fetch_one('SELECT * FROM patients WHERE patient_id = %s', (patient_id,))
    if not patient:
        flash('Patient not found.', 'danger')
        return redirect(url_for('patients'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        gender = request.form.get('gender', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        disease = request.form.get('disease', '').strip()

        if not all([name, age, gender, phone, address, disease]):
            flash('All fields are required.', 'danger')
            return render_template('edit_patient.html', patient=patient)

        execute_query(
            '''UPDATE patients
               SET name=%s, age=%s, gender=%s, phone=%s, address=%s, disease=%s
               WHERE patient_id=%s''',
            (name, age, gender, phone, address, disease, patient_id)
        )
        flash('Patient updated successfully.', 'success')
        return redirect(url_for('patients'))

    return render_template('edit_patient.html', patient=patient)


@app.route('/patients/delete/<int:patient_id>')
@login_required
def delete_patient(patient_id):
    execute_query('DELETE FROM patients WHERE patient_id = %s', (patient_id,))
    flash('Patient deleted successfully.', 'info')
    return redirect(url_for('patients'))


@app.route('/doctors')
@login_required
def doctors():
    search = request.args.get('search', '').strip()
    if search:
        doctors_list = fetch_all(
            '''SELECT * FROM doctors
               WHERE name LIKE %s OR specialization LIKE %s
               ORDER BY doctor_id DESC''',
            (f'%{search}%', f'%{search}%')
        )
    else:
        doctors_list = fetch_all('SELECT * FROM doctors ORDER BY doctor_id DESC')
    return render_template('doctors.html', doctors=doctors_list, search=search)


@app.route('/doctors/add', methods=['GET', 'POST'])
@login_required
def add_doctor():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        specialization = request.form.get('specialization', '').strip()
        phone = request.form.get('phone', '').strip()
        room_no = request.form.get('room_no', '').strip()

        if not all([name, specialization, phone, room_no]):
            flash('All fields are required.', 'danger')
            return render_template('add_doctor.html')

        execute_query(
            'INSERT INTO doctors (name, specialization, phone, room_no) VALUES (%s, %s, %s, %s)',
            (name, specialization, phone, room_no)
        )
        flash('Doctor added successfully.', 'success')
        return redirect(url_for('doctors'))

    return render_template('add_doctor.html')


@app.route('/doctors/edit/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def edit_doctor(doctor_id):
    doctor = fetch_one('SELECT * FROM doctors WHERE doctor_id = %s', (doctor_id,))
    if not doctor:
        flash('Doctor not found.', 'danger')
        return redirect(url_for('doctors'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        specialization = request.form.get('specialization', '').strip()
        phone = request.form.get('phone', '').strip()
        room_no = request.form.get('room_no', '').strip()

        if not all([name, specialization, phone, room_no]):
            flash('All fields are required.', 'danger')
            return render_template('edit_doctor.html', doctor=doctor)

        execute_query(
            'UPDATE doctors SET name=%s, specialization=%s, phone=%s, room_no=%s WHERE doctor_id=%s',
            (name, specialization, phone, room_no, doctor_id)
        )
        flash('Doctor updated successfully.', 'success')
        return redirect(url_for('doctors'))

    return render_template('edit_doctor.html', doctor=doctor)


@app.route('/doctors/delete/<int:doctor_id>')
@login_required
def delete_doctor(doctor_id):
    execute_query('DELETE FROM doctors WHERE doctor_id = %s', (doctor_id,))
    flash('Doctor deleted successfully.', 'info')
    return redirect(url_for('doctors'))


@app.route('/appointments')
@login_required
def appointments():
    status = request.args.get('status', '').strip()
    base_query = '''
        SELECT a.appointment_id, a.appointment_date, a.appointment_time, a.status,
               p.name AS patient_name, d.name AS doctor_name, d.specialization
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
    '''
    if status:
        appts = fetch_all(base_query + ' WHERE a.status = %s ORDER BY a.appointment_date DESC, a.appointment_time DESC', (status,))
    else:
        appts = fetch_all(base_query + ' ORDER BY a.appointment_date DESC, a.appointment_time DESC')
    return render_template('appointments.html', appointments=appts, status=status)


@app.route('/appointments/add', methods=['GET', 'POST'])
@login_required
def add_appointment():
    patients_list = fetch_all('SELECT patient_id, name FROM patients ORDER BY name')
    doctors_list = fetch_all('SELECT doctor_id, name, specialization FROM doctors ORDER BY name')

    if request.method == 'POST':
        patient_id = request.form.get('patient_id', '').strip()
        doctor_id = request.form.get('doctor_id', '').strip()
        appointment_date = request.form.get('appointment_date', '').strip()
        appointment_time = request.form.get('appointment_time', '').strip()
        status = request.form.get('status', '').strip()

        if not all([patient_id, doctor_id, appointment_date, appointment_time, status]):
            flash('All fields are required.', 'danger')
            return render_template('add_appointment.html', patients=patients_list, doctors=doctors_list)

        execute_query(
            '''INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status)
               VALUES (%s, %s, %s, %s, %s)''',
            (patient_id, doctor_id, appointment_date, appointment_time, status)
        )
        flash('Appointment booked successfully.', 'success')
        return redirect(url_for('appointments'))

    return render_template('add_appointment.html', patients=patients_list, doctors=doctors_list)


@app.route('/appointments/edit/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def edit_appointment(appointment_id):
    appointment = fetch_one('SELECT * FROM appointments WHERE appointment_id = %s', (appointment_id,))
    if not appointment:
        flash('Appointment not found.', 'danger')
        return redirect(url_for('appointments'))

    patients_list = fetch_all('SELECT patient_id, name FROM patients ORDER BY name')
    doctors_list = fetch_all('SELECT doctor_id, name, specialization FROM doctors ORDER BY name')

    if request.method == 'POST':
        patient_id = request.form.get('patient_id', '').strip()
        doctor_id = request.form.get('doctor_id', '').strip()
        appointment_date = request.form.get('appointment_date', '').strip()
        appointment_time = request.form.get('appointment_time', '').strip()
        status = request.form.get('status', '').strip()

        if not all([patient_id, doctor_id, appointment_date, appointment_time, status]):
            flash('All fields are required.', 'danger')
            return render_template('edit_appointment.html', appointment=appointment, patients=patients_list, doctors=doctors_list)

        execute_query(
            '''UPDATE appointments
               SET patient_id=%s, doctor_id=%s, appointment_date=%s, appointment_time=%s, status=%s
               WHERE appointment_id=%s''',
            (patient_id, doctor_id, appointment_date, appointment_time, status, appointment_id)
        )
        flash('Appointment updated successfully.', 'success')
        return redirect(url_for('appointments'))

    return render_template('edit_appointment.html', appointment=appointment, patients=patients_list, doctors=doctors_list)


@app.route('/appointments/delete/<int:appointment_id>')
@login_required
def delete_appointment(appointment_id):
    execute_query('DELETE FROM appointments WHERE appointment_id = %s', (appointment_id,))
    flash('Appointment deleted successfully.', 'info')
    return redirect(url_for('appointments'))


@app.errorhandler(Exception)
def handle_exception(error):
    return render_template('error.html', error=error), 500


if __name__ == '__main__':
    app.run(debug=True)
