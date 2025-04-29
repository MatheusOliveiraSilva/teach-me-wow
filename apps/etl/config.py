import os, json, time, requests, pandas as pd
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

REGION       = os.getenv("BLIZZ_REGION", "us")
BLIZZ_API    = f"https://{REGION}.api.blizzard.com"
NAMESPACE    = f"static-{REGION}"
LOCALE       = os.getenv("BLIZZ_LOCALE", "en_US")
BLIZZ_TOKEN_URL = f"https://{REGION}.battle.net/oauth/token"

CLIENT_ID        = os.getenv("BLIZZ_CLIENT_ID")
CLIENT_SECRET    = os.getenv("BLIZZ_CLIENT_SECRET")
CACHE_FILE    = Path(".blizz_token_cache.json")