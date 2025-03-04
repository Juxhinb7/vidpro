import time
from typing import List


from fastapi import FastAPI

from app.router.ffmpeg_router import ffmpeg_router
from app.service.user_service import UserService
from app.router.user_router import user_router
from app.schema.user import UserCreate, UserResponse

app = FastAPI()

@app.get("/v2/users", response_model=List[UserResponse])
async def read_users():
    start_time = time.perf_counter()
    users = await UserService.get_users()
    end_time = time.perf_counter()
    print(f"Query executed in {end_time - start_time:.6f} seconds")
    users = [{"id": user[0], "username": user[1], "email": user[2], "password": user[3]} for user in users]
    return users


@app.post("/v2/users/create")
def create_user(user_create: UserCreate) -> UserCreate:
    UserService.create_user(user_create.username, user_create.email, user_create.password)
    return user_create



app.include_router(user_router)
app.include_router(ffmpeg_router)