from fastapi import APIRouter, Depends, HTTPException
from django.contrib.auth import get_user_model
import django
import os
import sys
from asgiref.sync import sync_to_async
from django.conf import settings
from fastapi_app.auth import verify_access_token

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoBridge.settings")
django.setup()

User = get_user_model()
router = APIRouter()

@router.get("/users")
async def get_users(user_email: str = Depends(verify_access_token)):
    users = await sync_to_async(lambda: list(User.objects.all().values("email", "first_name", "last_name")))()
    if not users:
        raise HTTPException(status_code=404, detail="No registered users found")
    return {"users": users}

@router.get("/health")
async def health_check():
    return {"status": "running"}