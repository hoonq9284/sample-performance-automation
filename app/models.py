from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    phone: str
    website: str
    province: str
    city: str
    district: str
    street: str
    zipcode: int
    createdAt: str
    updatedAt: str

class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    phone: str
    website: str
    province: str
    city: str
    district: str
    street: str
    zipcode: int