from fastapi import APIRouter, Body, HTTPException,status
from fastapi.encoders import jsonable_encoder
from src.CRUD import retrieve_user_username,retrieve_users,delete_user,add_user,update_user,login_user,retrieve_user_email
from src.schemas import UserSchema,UpdateUserModel,ResponseModel,ErrorResponseModel
from src.database import hash_password,create_refresh_token,create_access_token,ALGORITHM,JWT_SECRET_KEY
from jose import jwt,JWTError
from pydantic import EmailStr
import random
from datetime import datetime


router = APIRouter()


@router.post("/sign_up", response_description="User data added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    user['email'] = user['email'].lower()
    if await retrieve_user_email(user['email']) == None and await retrieve_user_username(user["username"]) == None:
        user['password'] = hash_password(user['password'])
        await add_user(user)
        return {
            "access_token": create_access_token(user['email']),
            "refresh_token": create_refresh_token(user['email']),
            "username": user['username'],
            "email": user['email']
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username exists"
        )


@router.get("/", response_description="User retrieved")
async def get_users():
    users = await retrieve_users()
    if users:
        return ResponseModel(users, "Users data retrieved successfully")
    return ResponseModel(users, "Empty list returned")


@router.get("/get_current_player", response_description="Get what type of user")
async def get_current_player(token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
        user_type = payload.get("sub")
        if "Guest" in user_type:
            return {"type":"Guest"}
        elif user_type is None:
            raise credentials_exception
        else:
            user = await retrieve_user_email(user_type)
            return {
                "type": "User",
                "username": user['username'],
                "email": user['email']
            }
    except JWTError:
        raise credentials_exception


@router.put("/{id}")
async def update_user_data(id: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(id, req)
    if updated_user:
        return ResponseModel(
            "User with ID: {} name update is successful".format(id),
            "User name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/{id}", response_description="User data deleted from the database")
async def delete_user_data(id: str):
    deleted_user = await delete_user(id)
    if deleted_user:
        return ResponseModel(
            "User with ID: {} removed".format(id), "User deleted successfully"
        )
    raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect id"
        )


@router.post("/login")
async def login(email:EmailStr = Body(...),password:str = Body(...)):
    user = await login_user(email, password)
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect email or password"
        )
    else:
        return {
            "access_token": create_access_token(email),
            "refresh_token": create_refresh_token(email),
            "username": user['username'],
            "email": user['email']
        }

@router.post("/sign_up_guest", response_description="Guest get jwt")
async def add_guest_data():
    random_id = str('Guest') + str(random.randint(1,100000)) + str(datetime.now())
    return {
        "access_token": create_access_token(random_id),
        "refresh_token": create_refresh_token(random_id)
    }