from dotenv import load_dotenv
import pathlib
import os
import jwt

BASE_DIR = pathlib.Path(__file__).resolve().parent
try:
    load_dotenv(BASE_DIR.parent / ".env.coordinates")
except:
    load_dotenv(BASE_DIR.parent / ".env")


def get_jwt_token(username):
    return jwt.encode(payload={"username": str(username), },
                      key=os.getenv("SECRET_KEY_COORDINATES"),
                      algorithm="HS256")


token = get_jwt_token('Rental of vehicles')
print(str(token))
