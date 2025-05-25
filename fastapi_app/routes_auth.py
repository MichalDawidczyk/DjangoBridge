import os
import django
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi_app.auth import create_access_token, verify_password, get_password_hash
from django.contrib.auth import get_user_model
from fastapi_app.schemas import UserCreate, LoginRequest, DeleteUserRequest
from asgiref.sync import sync_to_async
from fastapi_app.auth import verify_access_token

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoBridge.settings")
django.setup()

User = get_user_model()
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.post("/register")
async def register_user(user: UserCreate):
    existing_user = await sync_to_async(lambda: User.objects.filter(email=user.email).exists())()
    if existing_user > 0:
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_password = get_password_hash(user.password)
    new_user = await sync_to_async(User.objects.create)(
        email=user.email, first_name=user.first_name, last_name=user.last_name, password=hashed_password
    )
    return {"message": "User registered successfully"}

@router.post("/login")
async def login_user(login_data: LoginRequest):
    user = await sync_to_async(lambda: User.objects.filter(email=login_data.email).first())()
    if not user or not await sync_to_async(verify_password)(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected-route")
async def protected_route(user_email: str = Depends(verify_access_token)):
    user = await sync_to_async(lambda: User.objects.filter(email=user_email).first())()
    if not user:
        raise HTTPException(status_code=404, detail="User not found or deleted")
    return {"message": f"Welcome {user_email}, you're authenticated!"}


@router.delete("/delete-user")
async def delete_user(request: DeleteUserRequest):
    user = await sync_to_async(lambda: User.objects.filter(email=request.email).first())()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await sync_to_async(user.delete)()

    return {"message": f"User {request.email} deleted successfully"}
