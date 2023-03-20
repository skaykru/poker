from .database import user_collection, user_helper ,verify_password
from bson.objectid import ObjectId
from pydantic import EmailStr


# Retrieve all users present in the database
async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


# Add a new user into to the database
async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


# Retrieve a student with a matching ID
async def retrieve_user(id: str) -> dict:
    user = await user_collection.find_one({"_id": id})
    if user:
        return user_helper(user)


# Retrieve a student with a matching email
async def retrieve_user_email(email: EmailStr) -> dict:
    email = email.lower()
    user = await user_collection.find_one({"email": email})
    if user:
        return user
    else:
        return None


async def retrieve_user_username(username: str) -> dict:
    user = await user_collection.find_one({"username": username})
    if user:
        return user
    else:
        return None


# Update a user with a matching ID
async def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


# Delete a user from the database
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": id})
    if user:
        await user_collection.delete_one({"_id": id})
        return True

# Login user
async def login_user(user_email: EmailStr,password:str) -> dict:
    user = await retrieve_user_email(user_email)
    if user == None:
        return None
    if verify_password(password,user['password']):
        return user
    else:
        return None