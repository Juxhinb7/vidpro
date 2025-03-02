from pydantic import EmailStr

from database import engine
from sqlalchemy import text


class UserService:
    @staticmethod
    async def get_users():
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT * FROM users"))
            users = result.fetchall()
            return users

    @staticmethod
    async def create_user(username: str, email: EmailStr, hashed_password: str):
        async with engine.connect() as conn:
            async with conn.begin():
                await conn.execute(text("INSERT INTO users (username, email, hashed_password) VALUES (:username, :email, :hashed_password)"), {"username": username, "email": email, "hashed_password": hashed_password})

    @staticmethod
    async def remove_user(user_id: int):
        async with engine.connect() as conn:
            conn.execute(text("DELETE FROM users WHERE users.id = :user_id"), {"user_id": user_id})