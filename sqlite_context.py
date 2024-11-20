import sqlite3

class SqliteConnection:

    def __init__(self, host):
        self.host = host
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.host)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()
