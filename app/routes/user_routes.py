from fastapi import APIRouter
from app.controllers.user_controller import UserController
from app.models.user_model import User

router = APIRouter(prefix="/users", tags=["Users"])

controller = UserController()


@router.post("/")
async def create_user(user: User):
    return controller.create_user(user)


@router.get("/{user_id}")
async def get_user(user_id: int):
    return controller.get_user(user_id)


@router.get("/")
async def get_users():
    return controller.get_users()


@router.put("/{user_id}")
async def update_user(user_id: int, user: User):
    return controller.update_user(user_id, user)


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    return controller.delete_user(user_id)
