from pydantic import EmailStr

from database import engine
from sqlalchemy import text
from app.model.serialization.user import User


class UserService:
    @staticmethod
    async def get_users():
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT * FROM users"))
            users = result.fetchall()
            return [User(id=user[0], username=user[1], email=user[2]) for user in users]

    @staticmethod
    async def get_user(username: str, email: EmailStr):
        async with engine.connect() as conn:
            result = await conn.execute(
                text(
                    "SELECT id, username, email, hashed_password FROM users WHERE username= :username AND email = :email"),
                {"username": username, "email": str(email)}
            )

            user = result.fetchone()

            if user:
                return {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "password": user[3]  # Now this actually contains the correct hashed password
                }

            return None

    @staticmethod
    async def get_user_by_email(email: str):
        async with engine.connect() as conn:
            try:
                # Query to check if the email exists
                result = await conn.execute(
                    text("SELECT * FROM users WHERE email = :email"),
                    {"email": email}
                )

                user = result.fetchone()

                if user:
                    # Return a dictionary instead of raw tuple for easier handling
                    return {
                        "id": user[0],  # Ensure the index is correct
                        "username": user[1],
                        "email": user[2]
                    }
                else:
                    return None
            except Exception as e:
                print(f"Error querying the database: {e}")
                return None

    @staticmethod
    async def create_user(username: str, email: EmailStr, hashed_password: str):
        async with engine.connect() as conn:
            async with conn.begin():
                await conn.execute(text("INSERT INTO users (username, email, hashed_password) VALUES (:username, :email, :hashed_password)"), {"username": username, "email": email, "hashed_password": hashed_password})

    @staticmethod
    async def remove_user(user_id: int):
        async with engine.connect() as conn:
            async with conn.begin():
                await conn.execute(text("DELETE FROM users WHERE users.id = :user_id"), {"user_id": user_id})

    @staticmethod
    async def user_exists(username: str, email: EmailStr):
        async with engine.connect() as conn:
            user = await conn.execute(text("SELECT 1 FROM users WHERE username=:username OR email = :email"), {"username": username, "email": email})
            return user.fetchone() is not None

