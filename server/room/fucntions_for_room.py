from .database import room_collection, room_helper
from src.CRUD import retrieve_user_email
from pydantic import EmailStr
from bson import ObjectId
from room.poker.poker import gen
from room.functions_for_poker import check_poker_hand
import random


def create_user_in_room_for_registration(id_number:int,username:str,start_game:int,start_tokens:int):
    player = dict()
    player.setdefault("id", id_number)
    player.setdefault("username", username)
    player.setdefault("status", "InGame")
    player.setdefault("start_game", start_game)
    player.setdefault("current_tokens", start_tokens)
    player.setdefault("cards", [])
    player.setdefault("current_points", 0)
    players = []
    players.append(player)
    return players


def create_user_in_room_for_entry_room(id_number:int,username:str,start_game:int,start_tokens:int):
    player = dict()
    player.setdefault("id", id_number)
    player.setdefault("username", username)
    player.setdefault("status", "InGame")
    player.setdefault("start_game", start_game)
    player.setdefault("current_tokens", start_tokens)
    player.setdefault("cards", [])
    player.setdefault("current_points", 0)
    return player

def guest_user_create_room(start_tokens:int):
    players = create_user_in_room_for_registration(1,str('Guest') + str(random.randint(1,100000)),1,start_tokens)
    return players


async def find_user(user_info:EmailStr,start_tokens:int) -> list:
    user = await retrieve_user_email(user_info)
    players = create_user_in_room_for_registration(1,user["username"], 1, start_tokens)
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


async def find_room_by_id(id:str)-> dict:
    room = await room_collection.find_one({"id": id})
    if room:
        return room
    else:
        return None


async def join_room(id: str,user_email:EmailStr):
    room = await room_collection.find_one({"_id": ObjectId(id)})
    players = []
    for player in room["players"]:
        players.append(player)
    user = await retrieve_user_email(user_email)
    player = create_user_in_room_for_entry_room(len(players)+1,user["username"],0,room["start_tokens"])
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
    player = create_user_in_room_for_entry_room(len(players)+1,str('Guest') + str(random.randint(1,100000)),0,room["start_tokens"])
    players.append(player)
    room["players"] = players
    if room:
        updated_room = await room_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": room}
        )
        if updated_room:
            return room_helper(room)
        return False


async def update_info_player_cards(id: str):
    room = await room_collection.find_one({"_id": ObjectId(id)})
    deck = gen()
    for i in range(len(room["players"])):
        cards = []
        cards.append(deck[0])
        cards.append(deck[1])
        room["players"][i]["cards"]= cards
        deck.remove(deck[0])
        deck.remove(deck[1])
    table_cards = [deck[i] for i in range(5)]
    for i in range(5):
        deck.remove(deck[i])
    room["table_cards"] = table_cards
    if room:
        updated_room = await room_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": room}
        )
        if updated_room:
            return room_helper(room)
        return False


async def total_score_of_round(id:str):
    room = await room_collection.find_one({"_id": ObjectId(id)})
    table_cards = room["table_cards"]
    all_results = []
    for i in range(len(room["players"])):
        player_hand = room["players"][i]["cards"] + table_cards
        current_point = check_poker_hand(player_hand)
        room["players"][i]["current_points"] = current_point
        all_results.append(current_point)
    maximalnui_bal = max(all_results)
    await room_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": room}
    )
    winer =[]
    for i in range(len(room["players"])):
        if room["players"][i]["current_points"] == maximalnui_bal:
            winer.append(room["players"][i]["id"])
    found_room = await end_of_the_game(id,winer)
    return winer,found_room #вертаємо нікнейми переможців

async def fold(id: str,position:int):
    room = await room_collection.find_one({"_id": ObjectId(id)})
    room["players"][position]["cards"]= []
    room["players"][position]["status"] = "fold"
    if room:
        updated_room = await room_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": room}
        )
        if updated_room:
            return room_helper(room)
        return False

async def blind(id: str,position:int):
    room = await room_collection.find_one({"_id": ObjectId(id)})
    a = room["players"][position]["current_tokens"]
    room["table_tokens"] += a
    room["players"][position]["current_tokens"] -= a
    if room:
        updated_room = await room_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": room}
        )
        if updated_room:
            return room_helper(room)
        return False

async def end_of_the_game(id: str,positions:list):
    room = await room_collection.find_one({"_id": ObjectId(id)})
    a = room["table_tokens"]
    for i in range(len(positions)):
        room["players"][i]["current_tokens"] += a/len(positions)
    for player in range(len(room["players"])):
        room["players"][player]["cards"] = []
        room["players"][player]["status"] = "InGame"
    room["table_tokens"] = 0
    if room:
        updated_room = await room_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": room}
        )
        if updated_room:
            return room_helper(room)
        return False