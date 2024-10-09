from flask import Flask, render_template, request, session, redirect, url_for, flash
from database import Database
from user import User
from admin import Admin
from appointment import Appointment

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Initialize the database
db = Database()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(db)
        return user.register(request.form['name'], request.form['email'], request.form['password'], 
                             request.form['phone'], request.form['address'])
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(db)
        return user.login(request.form['email'], request.form['password'])
    return render_template('login.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin = Admin(db)
        return admin.login(request.form['username'], request.form['password'])
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' not in session:
        flash("Please log in as an admin to access this page.", "warning")
        return redirect(url_for('admin_login'))

    admin = Admin(db)
    services = admin.get_services()
    appointments = admin.get_appointments()
    return render_template('admin_dashboard.html', services=services, appointments=appointments)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for('login'))
    
    services = db.execute_query('SELECT * FROM services', fetchall=True)
    return render_template('dashboard.html', services=services)

@app.route('/book', methods=['POST'])
def book():
    if 'user_id' not in session:
        flash("Please log in to book an appointment.", "warning")
        return redirect(url_for('login'))
    
    appointment = Appointment(db)
    return appointment.book(session['user_id'], request.form['service_id'], request.form['appointment_time'])

@app.route('/appointments')
def appointments():
    if 'user_id' not in session:
        flash("Please log in to view your appointments.", "warning")
        return redirect(url_for('login'))
    
    appointment = Appointment(db)
    return appointment.view_appointments(session['user_id'])

@app.route('/add_service', methods=['POST'])
def add_service():
    if 'admin' not in session:
        flash("Please log in as an admin to access this page.", "warning")
        return redirect(url_for('admin_login'))

    service_name = request.form['service_name']
    price = request.form['price']
    admin = Admin(db)
    admin.add_service(service_name, price)
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
