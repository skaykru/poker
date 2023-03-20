from fastapi import APIRouter,WebSocket,WebSocketDisconnect
from jose import jwt, JWTError
from src.database import JWT_SECRET_KEY,ALGORITHM
from fastapi import HTTPException,status
from room.fucntions_for_room import create_room,join_room,find_user,guest_user_create_room,\
    find_room,join_room_for_guest

router = APIRouter()


@router.websocket("/ws/create_room")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json(mode = 'text')
            token = data["jwt"]
            try:
                credentials_exception = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
                payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
                user_type = payload.get("sub")
            except JWTError:
                raise credentials_exception

            if data['event_type'] == 'CreateRoom':
                if "Guest" in user_type:
                    player = guest_user_create_room(data["room_info"]["start_tokens"])
                    room_data: dict = data["room_info"]
                    room_data.setdefault("players", player)
                    room_data.setdefault("turn_player_index",1)
                    room = await create_room(room_data)
                    r_data= {"room":room,"event_type":"RoomCreated"}
                    await websocket.send_json(r_data)
                else:
                    player = await find_user(user_type,data["room_info"]["start_tokens"])
                    room_data:dict = data["room_info"]
                    room_data.setdefault("players",player)
                    room_data.setdefault("turn_player_index",1)
                    room = await create_room(room_data)
                    r_data= {"room":room,"event_type":"RoomCreated"}
                    await websocket.send_json(r_data)


            if data['event_type'] == 'FindRoom':
                found_rooms = await find_room(data["room_info"]["room_name"])
                r_data = {"rooms": found_rooms, "event_type": "RoomsFound"}
                await websocket.send_json(r_data)


            if data['event_type'] == 'JoinRoom':
                if "Guest" in user_type:
                    room = await join_room_for_guest(data["room_info"]["id"])
                    r_data= {"room":room,"event_type":"JoinedToRoom"}
                    await websocket.send_json(r_data)
                else:
                    room = await join_room(data["room_info"]["id"],user_type)
                    r_data= {"room":room,"event_type":"JoinedToRoom"}
                    await websocket.send_json(r_data)


    except WebSocketDisconnect:
        await websocket.send_text(f"Client left the room")