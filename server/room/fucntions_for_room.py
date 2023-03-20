from .database import room_collection, room_helper
from src.CRUD import retrieve_user_email
from pydantic import EmailStr
from bson import ObjectId
import random


def create_user_in_room(id_number:int,username:str,start_game:int,start_tokens:int):
    player = dict()
    player.setdefault("id", id_number)
    player.setdefault("username", username)
    player.setdefault("status", "InGame")
    player.setdefault("start_game", start_game)
    player.setdefault("current_tokens", start_tokens)
    players = []
    players.append(player)
    return players

def guest_user_create_room(start_tokens:int):
    players = create_user_in_room(1,str('Guest') + str(random.randint(1,100000)),1,start_tokens)
    return players


async def find_user(user_info:EmailStr,start_tokens:int) -> list:
    user = await retrieve_user_email(user_info)
    players = create_user_in_room(1,user["username"], 1, start_tokens)
    players[0]["id"] = user_info
    return players


async def create_room(room_data: dict) -> dict:
    room = await room_collection.insert_one(room_data)
    new_room = await room_collection.find_one({"_id": room.inserted_id})
    return room_helper(new_room)


async def find_room(room_name:str) -> list:
    rooms = []
    async for room in room_collection.find({"room_name": room_name}):
        rooms.append(room_helper(room))
    return rooms


async def join_room(id: str,user_email:EmailStr):
    room = await room_collection.find_one({"_id": ObjectId(id)})
    players = []
    for player in room["players"]:
        players.append(player)
    user = await retrieve_user_email(user_email)
    player = create_user_in_room(len(players)+1,user["username"],0,room["start_tokens"])
    players.append(player)
    room["players"] = players
    if room:
        updated_room = await room_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": room}
        )
        if updated_room:
            return room_helper(room)
        return False


async def join_room_for_guest(id: str):
    room = await room_collection.find_one({"_id": ObjectId(id)})
    players = []
    for player in room["players"]:
        players.append(player)
    player = create_user_in_room(len(players)+1,str('Guest') + str(random.randint(1,100000)),0,room["start_tokens"])
    players.append(player)
    room["players"] = players
    if room:
        updated_room = await room_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": room}
        )
        if updated_room:
            return room_helper(room)
        return False