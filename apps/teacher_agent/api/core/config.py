import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL", "postgresql://user:password@localhost:5432/teachmewowdb")
API_PREFIX = "/api/v1" 