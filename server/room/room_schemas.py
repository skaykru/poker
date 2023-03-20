from pydantic import BaseModel,EmailStr,Field
from typing import Optional


class RoomSchema(BaseModel):
    players: dict = Field(...)
    blind: str = Field(...)
    turn_player_index : int = Field(...)
    room_name : str = Field(...)


class UpdateRoomModel(BaseModel):
    players: Optional[dict]
    blind: Optional[str]
    turn_player_index: Optional[int]
    room_name: Optional[str]