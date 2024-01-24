from dotenv import load_dotenv
import sqlite3
import pathlib
import os
import jwt

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
try:
    load_dotenv(BASE_DIR / ".env.coordinates")
except:
    load_dotenv(BASE_DIR / "../.env")

connection = sqlite3.connect(os.getenv('COORDINATES_DATABASE_URI'))

with open(BASE_DIR / 'CoordinatesAPI/users.sql') as f:
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


token = get_jwt_token(user[0], user[2])
os.environ["COORDINATES_API_KEY"] = str(token)
print(token)
