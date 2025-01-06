from unittest.mock import Mock, patch
import pytest
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal

@pytest.fixture(scope="function")
def db_session():
    """Fixture to provide a database session for testing."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_get_db(db_session):
    """Test the get_db function to ensure it yields a valid session."""
    db_generator = get_db()
    db_instance = next(db_generator)
    
    assert isinstance(db_instance, Session)
    db_generator.close()

@patch("app.database.SessionLocal", return_value=Mock(Session))  
def test_get_db(mock_session_local):  
    """Test the get_db function to ensure it yields a valid session."""  

    # Test if get_db return a generator  
    assert hasattr(get_db(), '__iter__')  

    db_generator = get_db()  
    db_instance = next(db_generator)  

    # Test if first output of the generator is a Session instance  
    assert isinstance(db_instance, Session)  

    # Test if SessionLocal was called once, creating a new session  
    mock_session_local.assert_called_once()  
    db_generator.close()  
