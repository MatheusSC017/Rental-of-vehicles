import sqlite3
import pathlib
from flask import current_app
from functools import wraps

pathlib.Path().resolve()


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
def get_user(cursor, user_id, username):
    cursor.execute("SELECT * FROM users WHERE id = (?) AND username = (?)", (user_id, username))
    return cursor.fetchone()
