from dotenv import load_dotenv
import sqlite3
import pathlib
import os

BASE_DIR = pathlib.Path(__file__).resolve().parent
try:
    load_dotenv(BASE_DIR.parent / ".env.coordinates")
except:
    load_dotenv(BASE_DIR.parent / ".env")

connection = sqlite3.connect(os.getenv('COORDINATES_DATABASE_URI'))

if os.path.isfile(BASE_DIR.parent / 'CoordinatesAPI/users.sql'):
    sql_file = BASE_DIR.parent / 'CoordinatesAPI/users.sql'
else:
    sql_file = BASE_DIR / 'users.sql'

with open(sql_file) as f:
    connection.executescript(f.read())

cursor = connection.cursor()

cursor.execute("INSERT INTO users (username) VALUES (?)", ('Rental of vehicles', ))

connection.commit()
connection.close()
