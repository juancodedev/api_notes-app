import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import timedelta, UTC
from jose import jwt, JWTError
from models import User
from schemas import UserCreate
from database import Base
from services.auth import (
    hash_password,
    verify_password,
    authenticate_user,
    create_access_token,
    register_user
)
import config

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_hash_password():
    password = "testpassword123"
    hashed = hash_password(password)
    assert hashed != password
    assert isinstance(hashed, str)
    assert len(hashed) > 20
    assert hash_password(password) != hash_password(password)

def test_verify_password():
    password = "testpassword123"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False
    
    assert verify_password("", hashed) is False

def test_authenticate_user(db):
    username = "testuser"
    password = "testpassword123"
    hashed_password = hash_password(password)
    
    test_user = User(
        username=username,
        name="Test User",
        password=hashed_password
    )
    db.add(test_user)
    db.commit()
    
    authenticated_user = authenticate_user(db, username, password)
    assert authenticated_user is not None
    assert authenticated_user.username == username
    
    wrong_auth = authenticate_user(db, username, "wrongpassword")
    assert wrong_auth is None
    
    nonexistent = authenticate_user(db, "nonexistent", password)
    assert nonexistent is None

def test_create_access_token():
    username = "testuser"
    test_data = {"sub": username}
    expires_delta = timedelta(minutes=30)
    
    token = create_access_token(test_data, expires_delta)
    
    assert isinstance(token, str)
    
    payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    assert payload["sub"] == username
    assert "exp" in payload

    short_token = create_access_token(test_data, timedelta(minutes=5))
    assert short_token != token  
    
    with pytest.raises(JWTError):
        jwt.decode(token, "wrong_key", algorithms=[config.ALGORITHM])

def test_register_user_duplicate_username(db):
    user_data = UserCreate(
        username="testuser",
        password="testpass123",
        name="Test User"
    )
    
    register_user(db, user_data)
    
    with pytest.raises(ValueError) as exc_info:
        register_user(db, user_data)
    assert "Username already registered" in str(exc_info.value)

def test_login_user_success(db):
    user_data = UserCreate(
        username="logintest",
        password="testpass123",
        name="Login Test User"
    )
    register_user(db, user_data)
    
    authenticated_user = authenticate_user(db, "logintest", "testpass123")
    assert authenticated_user is not None
    assert authenticated_user.username == "logintest"
    assert authenticated_user.name == "Login Test User"

def test_login_user_invalid_credentials(db):
    user_data = UserCreate(
        username="invalidtest",
        password="testpass123",
        name="Invalid Test User"
    )
    register_user(db, user_data)
    
    authenticated_user = authenticate_user(db, "invalidtest", "wrongpass")
    assert authenticated_user is None

def test_login_user_nonexistent_user(db):
    authenticated_user = authenticate_user(db, "nonexistentuser", "anypassword")
    assert authenticated_user is None
