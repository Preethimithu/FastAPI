from typing import List
from uuid import uuid4, UUID
from fastapi import FastAPI, HTTPException

from models import User, Gender, Role, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(id=uuid4(),
         first_name="Anto",
         last_name="mithula",
         gender=Gender.female,
         roles=[Role.admin]
         ),
    User(id=uuid4(),
         first_name="Sravani",
         last_name="bestha",
         gender=Gender.female,
         roles=[Role.student]
         )
]


@app.get("/")
async def root():
# that enables code to run separately from the main application
    return {"Hello": "Preethi"}


@app.get("/api/v1/users")
async def fetch_users():
    return db;


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "gender": user.gender,
            "roles": user.roles}


@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id:UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )