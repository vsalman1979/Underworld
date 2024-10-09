from flask import flash, session, redirect, url_for
from database import Database

class Admin:
    def __init__(self, db: Database):
        self.db = db

    def login(self, username: str, password: str):
        # Fetch the admin details from the database
        admin = self.db.execute_query('SELECT * FROM admin WHERE username = ?', (username,), fetchone=True)
        
        if admin and admin['password'] == password:  # Compare with plain text password
            session['admin'] = True
            flash("Admin logged in successfully!", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid admin credentials.", "danger")
            return redirect(url_for('admin_login'))  # Redirect to login page on failure

    def logout(self):
        session.pop('admin', None)  # Remove admin session
        flash("You have been logged out.", "info")
        return redirect(url_for('admin_login'))  # Redirect to admin login page

    def add_service(self, service_name: str, price: float):
        try:
            # Insert new service into the services table
            self.db.execute_query(
                'INSERT INTO services (service_name, price) VALUES (?, ?)',
                (service_name, price))
            flash("Service added successfully!", "success")
        except Exception as e:
            flash(f"An error occurred while adding the service: {str(e)}", "danger")

    def get_services(self):
        # Fetch all services from the database
        services = self.db.execute_query('SELECT * FROM services', fetchall=True)
        return services

    def get_appointments(self):
        # Fetch all appointments from the database
        appointments = self.db.execute_query('''
            SELECT appointments.*, users.name AS user_name 
            FROM appointments 
            JOIN users ON appointments.user_id = users.id
            ORDER BY appointment_time DESC  -- Optional: Order by appointment time
        ''', fetchall=True)
        return appointments
