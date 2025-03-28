from fastapi import FastAPI
from routers import auth, notes, tags
from fastapi.middleware.cors import CORSMiddleware
from services.notes import initialize_db
from database import get_db

app = FastAPI()

origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,  
    allow_methods=["*"],
    allow_headers=["*"],  
)

@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    initialize_db(db)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(notes.router, prefix="/api/notes")
app.include_router(tags.router, prefix="/tags", tags=["tags"])
