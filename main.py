from fastapi import FastAPI
from routers import auth, notes

app = FastAPI()

app.include_router(auth.router, prefix="/api/auth")
app.include_router(notes.router, prefix="/api/notes")
