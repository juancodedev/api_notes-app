from fastapi import FastAPI
from routers import auth, notes
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(auth.router, prefix="/api/auth")
app.include_router(notes.router, prefix="/api/notes")
