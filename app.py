from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('haircut_booking.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Customer registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (name, email, password, phone, address) VALUES (?, ?, ?, ?, ?)',
                         (name, email, password, phone, address))
            conn.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("User already exists with this email.", "danger")
        finally:
            conn.close()
    return render_template('register.html')

# Customer login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.", "danger")
    
    return render_template('login.html')

# Admin login
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if admin:
            session['admin'] = True
            flash("Admin logged in successfully!", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid admin credentials.", "danger")
    
    return render_template('admin_login.html')

# Admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' not in session:
        flash("Please log in as admin.", "warning")
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM services').fetchall()
    appointments = conn.execute('''
        SELECT appointments.id, users.name as user_name, services.service_name, appointments.appointment_time
        FROM appointments
        JOIN users ON appointments.user_id = users.id
        JOIN services ON appointments.service_id = services.id
    ''').fetchall()
    conn.close()
    
    return render_template('admin_dashboard.html', services=services, appointments=appointments)

# Add service (admin)
@app.route('/add_service', methods=['POST'])
def add_service():
    if 'admin' not in session:
        flash("Please log in as admin.", "warning")
        return redirect(url_for('admin_login'))
    
    service_name = request.form['service_name']
    price = request.form['price']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO services (service_name, price) VALUES (?, ?)', (service_name, price))
    conn.commit()
    conn.close()
    
    flash("Service added successfully!", "success")
    return redirect(url_for('admin_dashboard'))

# Customer dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM services').fetchall()
    conn.close()
    
    return render_template('dashboard.html', services=services)

# Book appointment (customer)
@app.route('/book', methods=['POST'])
def book():
    if 'user_id' not in session:
        flash("Please log in to book an appointment.", "warning")
        return redirect(url_for('login'))
    
    service_id = request.form['service_id']
    appointment_time = request.form['appointment_time']
    user_id = session['user_id']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO appointments (user_id, service_id, appointment_time) VALUES (?, ?, ?)', 
                 (user_id, service_id, appointment_time))
    conn.commit()
    conn.close()

    flash("Appointment booked successfully!", "success")
    return redirect(url_for('dashboard'))

# View appointments (customer)
@app.route('/appointments')
def appointments():
    if 'user_id' not in session:
        flash("Please log in to view your appointments.", "warning")
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    appointments = conn.execute('''
        SELECT appointments.id, services.service_name, appointments.appointment_time 
        FROM appointments 
        JOIN services ON appointments.service_id = services.id
        WHERE user_id = ?''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('appointments.html', appointments=appointments)

# Logout (customer/admin)
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
