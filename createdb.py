import sqlite3

conn = sqlite3.connect('haircut_booking.db')
cur = conn.cursor()

# Create users table (customers)
cur.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                phone TEXT,
                address TEXT
                )''')

# Create services table
cur.execute('''CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_name TEXT NOT NULL,
                price REAL NOT NULL
                )''')

# Create appointments table
cur.execute('''CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                service_id INTEGER,
                appointment_time TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(service_id) REFERENCES services(id)
                )''')

# Create admin table
cur.execute('''CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
                )''')

# Insert default admin user
cur.execute('''INSERT OR IGNORE INTO admin (username, password) VALUES ('admin', 'admin123')''')

# Insert some default services
cur.execute('''INSERT OR IGNORE INTO services (service_name, price) VALUES ('Trim', 15.0)''')
cur.execute('''INSERT OR IGNORE INTO services (service_name, price) VALUES ('Full Cut', 25.0)''')
cur.execute('''INSERT OR IGNORE INTO services (service_name, price) VALUES ('Coloring', 45.0)''')

conn.commit()
conn.close()
