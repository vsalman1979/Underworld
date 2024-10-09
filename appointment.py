from flask import flash, redirect, url_for, render_template
from database import Database

class Appointment:
    def __init__(self, db):
        self.db = db

    def book(self, user_id, service_id, appointment_time):
        self.db.execute_query('INSERT INTO appointments (user_id, service_id, appointment_time) VALUES (?, ?, ?)', 
                              (user_id, service_id, appointment_time))
        flash("Appointment booked successfully!", "success")
        return redirect(url_for('dashboard'))

    def view_appointments(self, user_id):
        appointments = self.db.execute_query('''
            SELECT appointments.id, services.service_name, appointments.appointment_time 
            FROM appointments 
            JOIN services ON appointments.service_id = services.id
            WHERE user_id = ?''', (user_id,), fetchall=True)
        return render_template('appointments.html', appointments=appointments)
