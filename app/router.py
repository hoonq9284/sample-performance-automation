from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from .models import User, UserCreate

router = APIRouter()

# 인메모리 저장소
_users: List[User] = []
_next_id = 1

# 유저를 찾는 함수
def find_user(user_id: int):
    for user in _users:
        if user.id == user_id:
            return user
    return None

# 유저 전체 조회
@router.get("/users", response_model=List[User])
def get_users():
    return _users

# 유저 단일 조회 (특정 유저 조회)
@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = find_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="ERROR: User Not Found")
    return user

# 유저 생성
@router.post("/users", response_model=User, status_code=201)
def create_user(user: UserCreate):
    global _next_id
    # 서버에서 id 생성 후 기존 id와 충돌 여부만 find_user로 확인
    new_id = _next_id
    if find_user(new_id) is not None:
        raise HTTPException(status_code=409, detail="ERROR: User is duplicated")
    _next_id += 1

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    created_user = User(
        id=new_id,
        name=user.name,
        username=user.username,
        email=user.email,
        phone=user.phone,
        website=user.website,
        province=user.province,
        city=user.city,
        district=user.district,
        street=user.street,
        zipcode=user.zipcode,
        createdAt=now,
        updatedAt=now,
    )
    _users.append(created_user)
    return created_user

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    user = find_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="ERROR: User Not Found")
    # 리스트엔 User 객체가 들어있으므로 객체 자체를 제거해야 함
    _users.remove(user)
    return {"message": f"User(id={user_id}) has been deleted."}