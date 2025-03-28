import os

DATABASE_URL = os.getenv("DB_URL","postgresql://postgres:5HOmZmsJ6Jhe6Ky@localhost:5432/notes_app")
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
