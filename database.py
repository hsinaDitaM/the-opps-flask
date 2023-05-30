from functools import wraps
from dataclasses import dataclass
import sqlite3

import os

LAYOUT = "schema.sql"

@dataclass
class User:
    def __init__(self, email, username, password, role):
        self.email = email
        self.username = username
        self.password = password
        self.role = role

    def __getitem__(self, key):
        return getattr(self, key)

class Database:
    #def __init__(self, path, table):
    def __init__(self, path):
        self.database_path = path

        if os.path.exists(path):
            self.connection = sqlite3.connect(path)
            self.cursor = self.connection.cursor()
        else:
            self.initialize_with(LAYOUT)

    def initialize_with(self, layout):
        self.connection = sqlite3.connect(self.database_path)
        with open(layout) as f:
            self.connection.executescript(f.read())
        cur = self.connection.cursor()
        cur.execute("INSERT INTO users (email, username, password, role) VALUES (?, ?, ?, ?)", (
                "admin@example.com",
                "admin",
                "admin",
                "admin",
            )
        )

        # inserting test users for testing purposes obviously lol
        cur.execute("INSERT INTO users (email, username, password, role) VALUES (?, ?, ?, ?)", (
                "user@example.com",
                "user",
                "user",
                "user",
            )
        )

        self.connection.commit()

    def user_exists(self, username):
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cur.fetchone()

    def register_user(self, email, username, password, role):
        cur = self.connection.cursor()
        cur.execute("INSERT INTO users (email, username, password, role) VALUES (?, ?, ?, ?)", (
                email,
                username,
                password,
                role,
            )
        )

        self.connection.commit()

    def get_password(self, username):
        cur = self.connection.cursor()
        cur.execute("SELECT password FROM users WHERE username = ?", (username,))
        return cur.fetchone()[0]

    def verify_password(self, username, password):
        true_password = self.get_password(username)
        print(f"{true_password=} {password=}")
        if true_password == password:
            return True
        return False
    
    def get_user(self, username):
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cur.fetchone()

    def get_all_users(self):
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM users")
        return cur.fetchall()

    def update_user(self, user_id, email, username, password, role):
        try:
            cur = self.connection.cursor()
            cur.execute("UPDATE users SET email = ?, username = ?, password = ?, role = ? WHERE id = ?", (
                    email,
                    username,
                    password,
                    role,
                    user_id,
                )
            )
            self.connection.commit()
            return True
        except:
            return False

    
    def delete_user(self, user_id):
        try:
            cur = self.connection.cursor()
            cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
            self.connection.commit()
            return True
        except:
            return False

def use_database(path):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            db = Database(path)
            return f(db, *args, **kwargs)
        return wrapper
    return decorator