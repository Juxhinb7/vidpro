from pydantic import EmailStr

from database import engine
from sqlalchemy import text


class UserService:
    @staticmethod
    def get_users():
        with engine.connect() as conn:
            return conn.execute(text("SELECT * FROM users")).fetchall()

    @staticmethod
    def create_user(username: str, email: EmailStr, hashed_password: str):
        with engine.connect() as conn:
            conn.execute(text("INSERT INTO users (username, email, hashed_password) VALUES (:username, :email, :hashed_password)"), {"username": username, "email": email, "hashed_password": hashed_password})
            conn.commit()

    @staticmethod
    def remove_user(user_id: int):
        with engine.connect() as conn:
            conn.execute(text("DELETE FROM users WHERE users.id = :user_id"), {"user_id": user_id})