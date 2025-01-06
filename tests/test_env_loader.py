import os
import pytest
from unittest.mock import patch
from app.utils.env_loader import load_env

def test_load_env_success(monkeypatch):
    # Define variáveis de ambiente necessárias para o teste
    monkeypatch.setenv("DATABASE_URL", "postgresql://db_user:db_pass123@localhost:5432/debts_db")
    monkeypatch.setenv("SECRET_KEY", "supersecretkey")
    monkeypatch.setenv("DB_USER", "db_user")
    monkeypatch.setenv("DB_PASS", "db_pass123")
    monkeypatch.setenv("DB_NAME", "debts_db")

    load_env()  # Chama a função que carrega as variáveis de ambiente

    assert os.getenv("DATABASE_URL") == "postgresql://db_user:db_pass123@localhost:5432/debts_db"
    assert os.getenv("SECRET_KEY") == "supersecretkey"
    assert os.getenv("DB_USER") == "db_user"
    assert os.getenv("DB_PASS") == "db_pass123"
    assert os.getenv("DB_NAME") == "debts_db"

@patch('os.getenv')  
@patch('dotenv.load_dotenv')  
def test_load_env(mock_load_dotenv, mock_getenv):  

    # Se todas as variáveis de ambiente estiverem configuradas  
    mock_getenv.side_effect = lambda var: 'mock_value'  

    try:  
        load_env()  
    except EnvironmentError:  
        pytest.fail("EnvironmentError foi levantado, mas não era esperado")  

    print(mock_load_dotenv.mock_calls)  # Printando chamadas para mock_load_dotenv  

    # Se qualquer variável de ambiente não estiver configurada  
    mock_getenv.side_effect = lambda var: 'mock_value' if var != 'DB_PASS' else None  

    with pytest.raises(EnvironmentError, match="Missing required environment variable: DB_PASS"):  
        load_env()  

    print(mock_load_dotenv.mock_calls)  # Printando chamadas para mock_load_dotenv após levantamento de exception  

def test_load_env():  
    with patch('os.getenv', return_value='mock_value'):  
        try:  
            load_env()  
        except EnvironmentError:  
            pytest.fail("EnvironmentError foi levantado, mas não era esperado")  
    with patch('os.getenv', side_effect= lambda var: 'mock_value' if var != 'DB_PASS' else None):  
        with pytest.raises(EnvironmentError, match="Missing required environment variable: DB_PASS"):  
            load_env()  