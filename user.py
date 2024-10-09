from flask import flash, session, redirect, url_for, render_template
from database import Database

class User:
    def __init__(self, db):
        self.db = db

    def register(self, name, email, password, phone, address):
        try:
            self.db.execute_query(
                'INSERT INTO users (name, email, password, phone, address) VALUES (?, ?, ?, ?, ?)',
                (name, email, password, phone, address))
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("User already exists with this email.", "danger")
        return render_template('register.html')

    def login(self, email, password):
        user = self.db.execute_query('SELECT * FROM users WHERE email = ? AND password = ?', (email, password), fetchone=True)
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.", "danger")
        return render_template('login.html')
