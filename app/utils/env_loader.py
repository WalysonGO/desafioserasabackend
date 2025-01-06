import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()

    # Valida se as principais variáveis estão configuradas
    required_env_vars = ["DATABASE_URL", "SECRET_KEY", "DB_USER", "DB_PASS", "DB_NAME"]
    for var in required_env_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Missing required environment variable: {var}")
