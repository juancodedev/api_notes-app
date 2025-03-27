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
    """Test that hash_password creates a hash different from the original password."""
    password = "testpassword123"
    hashed = hash_password(password)
    
    # Hash should be different from original password
    assert hashed != password
    
    # Hash should be a string
    assert isinstance(hashed, str)
    
    # Hash should be long enough to be a bcrypt hash
    assert len(hashed) > 20
    
    # Different calls should produce different hashes
    assert hash_password(password) != hash_password(password)

def test_verify_password():
    """Test that verify_password correctly verifies passwords."""
    password = "testpassword123"
    hashed = hash_password(password)
    
    # Should return True for correct password
    assert verify_password(password, hashed) is True
    
    # Should return False for incorrect password
    assert verify_password("wrongpassword", hashed) is False
    
    # Should return False for empty password
    assert verify_password("", hashed) is False

def test_authenticate_user(db):
    """Test user authentication with valid and invalid credentials."""
    # Create a test user
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
    
    # Test successful authentication
    authenticated_user = authenticate_user(db, username, password)
    assert authenticated_user is not None
    assert authenticated_user.username == username
    
    # Test failed authentication with wrong password
    wrong_auth = authenticate_user(db, username, "wrongpassword")
    assert wrong_auth is None
    
    # Test failed authentication with non-existent user
    nonexistent = authenticate_user(db, "nonexistent", password)
    assert nonexistent is None

def test_create_access_token():
    """Test JWT token creation and verification."""
    # Test data for token
    username = "testuser"
    test_data = {"sub": username}
    expires_delta = timedelta(minutes=30)
    
    # Create token
    token = create_access_token(test_data, expires_delta)
    
    # Token should be a string
    assert isinstance(token, str)
    
    # Verify token can be decoded and contains correct data
    payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    assert payload["sub"] == username
    assert "exp" in payload  # Verify expiration is included
    
    # Test with different expiration
    short_token = create_access_token(test_data, timedelta(minutes=5))
    assert short_token != token  # Should be different tokens
    
    # Try decoding token with wrong key (should fail)
    with pytest.raises(JWTError):
        jwt.decode(token, "wrong_key", algorithms=[config.ALGORITHM])

def test_register_user_duplicate_username(db):
    """Test that registering a user with a duplicate username fails."""
    user_data = UserCreate(
        username="testuser",
        password="testpass123",
        name="Test User"
    )
    
    # Register first user
    register_user(db, user_data)
    
    # Try to register second user with same username
    with pytest.raises(ValueError) as exc_info:
        register_user(db, user_data)
    assert "Username already registered" in str(exc_info.value)

def test_login_user_success(db):
    """Test successful user login."""
    # Create test user
    user_data = UserCreate(
        username="logintest",
        password="testpass123",
        name="Login Test User"
    )
    register_user(db, user_data)
    
    # Test login
    authenticated_user = authenticate_user(db, "logintest", "testpass123")
    assert authenticated_user is not None
    assert authenticated_user.username == "logintest"
    assert authenticated_user.name == "Login Test User"

def test_login_user_invalid_credentials(db):
    """Test login with invalid password."""
    # Create test user
    user_data = UserCreate(
        username="invalidtest",
        password="testpass123",
        name="Invalid Test User"
    )
    register_user(db, user_data)
    
    # Test login with wrong password
    authenticated_user = authenticate_user(db, "invalidtest", "wrongpass")
    assert authenticated_user is None

def test_login_user_nonexistent_user(db):
    """Test login with nonexistent username."""
    authenticated_user = authenticate_user(db, "nonexistentuser", "anypassword")
    assert authenticated_user is None
