import sqlite3
from flask import current_app
from functools import wraps


def sqlite_connection(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        connection = sqlite3.connect(current_app.config['DATABASE_URI'])
        cursor = connection.cursor()

        result = f(cursor, *args, **kwargs)

        connection.commit()
        connection.close()

        return result
    return decorated


@sqlite_connection
def get_user(cursor, username):
    cursor.execute("SELECT * FROM users WHERE username = (?)", (username, ))
    return cursor.fetchone()
