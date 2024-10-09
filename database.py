import sqlite3
from flask import flash

class Database:
    def __init__(self):
        self.db_name = 'haircut_booking.db'

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def execute_query(self, query, args=(), fetchone=False, fetchall=False):
        conn = self.get_connection()
        result = None
        try:
            cur = conn.execute(query, args)
            conn.commit()
            if fetchone:
                result = cur.fetchone()
            elif fetchall:
                result = cur.fetchall()
        except sqlite3.Error as e:
            flash(str(e), "danger")
        finally:
            conn.close()
        return result
