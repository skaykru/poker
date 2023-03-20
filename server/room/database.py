import motor.motor_asyncio
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt


MONGO_DETAILS = "mongodb+srv://ukhachdenys:qewadszcx@cluster0.0txbgyh.mongodb.net/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
db = client.room

room_collection = db.get_collection("room_collection")

def room_helper(room) -> dict:
    return {
        "id": str(room["_id"]),
        "room_name": room["room_name"],
        "blind": room["blind"],
        "start_tokens":room["start_tokens"],
        "turn_player_index": room["turn_player_index"],
        "players": list(room["players"])
    }