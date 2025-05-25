from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

class LoginRequest(BaseModel):
    email: str
    password: str

class DeleteUserRequest(BaseModel):
    email: str