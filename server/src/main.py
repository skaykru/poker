from fastapi import FastAPI
from src.schemas import UserSchema
import uvicorn
from src.routes.user import router as UserRouter
from fastapi.middleware.cors import CORSMiddleware
from room.routes.room import router as RoomRouter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

app.include_router(UserRouter, tags=["User"], prefix="/user")
app.include_router(RoomRouter, tags=["Room"], prefix="/room")

@app.get('/')
def home():
    return {"key":"hello"}


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)