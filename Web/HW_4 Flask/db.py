import sqlite3
import threading
from config import db_path
class DB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()
        self.lock = threading.Lock()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS messages
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      time TEXT,
                      username TEXT,
                      message TEXT)''')
        self.conn.commit()

    def add_message(self, time, username, message):
        with self.lock, self.conn:
            print(f'{time} зашло')
            c = self.conn.cursor()
            print('в курсор зайшло')
            c.execute("INSERT INTO messages (time, username, message) VALUES (?, ?, ?)",
                      (time, username, message))
            self.conn.commit()

    def close(self):
        self.conn.close()

db = DB(db_path)