import sqlite3

class DB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS messages
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      time TEXT,
                      username TEXT,
                      message TEXT)''')
        self.conn.commit()

    def add_message(self, time, username, message):
        c = self.conn.cursor()
        c.execute("INSERT INTO messages (time, username, message) VALUES (?, ?, ?)",
                  (time, username, message))
        self.conn.commit()

    def close(self):
        self.conn.close()
