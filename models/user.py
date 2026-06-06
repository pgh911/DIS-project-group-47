import re
import sqlite3
from database import db_connection
from flask_login import UserMixin

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@(group47|gruppe47)\.[a-zA-Z]{2,}$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d).{8,}$')

class User(UserMixin):
    def __init__(self, row: sqlite3.Row) -> None:
        self.id: int = row["id"]
        self.username: str = row["username"]

    def get_id(self) -> str:
        return str(self.id)

def validate_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))

# ikke sikkert at password skal have regex
def validate_password(password: str) -> bool:
    return bool(PASSWORD_REGEX.match(password))

def list_users() -> list[User]:
    conn = db_connection()
    db_users = conn.execute(
        "SELECT * FROM users ORDER BY id"
    ).fetchall()
    conn.close()

    users: list[User] = []
    for db_user in db_users:
        users.append(User(db_user))
    return users
    
def get_user(id: int) -> User | None:
    conn = db_connection()
    db_user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (id,)
    ).fetchone()
    conn.close()

    if db_user:
        return User(db_user)
    return None
    
def create_user(email: str, password: str) -> int | None:
    if not validate_email(email):
        raise ValueError("Email must be in the format: name@group47.domain")

    conn = db_connection()

    existing = conn.execute(
        "SELECT id FROM users WHERE username = ?",
        (email,)
    ).fetchone()

    if existing:
        conn.close()
        raise ValueError("A user with that email already exists")

    cur = conn.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (email, password)
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id


def login(username: str, password: str) -> sqlite3.Row | None:
    conn = db_connection()
    db_user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    ).fetchone()
    conn.close()
    return db_user


def delete_user(id: int) -> None:
    conn = db_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    conn.close()
