from dotenv import load_dotenv
import sqlite3
import pathlib
import os
import jwt

load_dotenv()
pathlib.Path().resolve()

connection = sqlite3.connect('database.db')

with open('users.sql') as f:
    connection.executescript(f.read())

cursor = connection.cursor()

cursor.execute("INSERT INTO users (username) VALUES (?)", ('Rental of vehicles', ))

cursor.execute("SELECT * FROM users WHERE id = (?)", (cursor.lastrowid, ))

user = cursor.fetchone()

connection.commit()
connection.close()


def get_jwt_token(user_id, username):
    return jwt.encode(payload={"user_id": str(user_id), "username": str(username)},
                      key=os.getenv("SECRET_KEY_COORDINATES"),
                      algorithm="HS256")


print(get_jwt_token(user[0], user[2]))
