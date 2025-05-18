from fastapi import APIRouter, Depends, HTTPException
from django.contrib.auth import get_user_model
import django
import os
import sys
from asgiref.sync import sync_to_async
from django.conf import settings

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoBridge.settings")
django.setup()

User = get_user_model()
router = APIRouter()

@router.get("/users")
async def get_users():
    users = await sync_to_async(list)(User.objects.all())
    return [{"email": user.email} for user in users]

@router.get("/health")
async def health_check():
    return {"status": "running"}