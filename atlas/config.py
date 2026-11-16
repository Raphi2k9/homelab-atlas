import os
from dotenv import load_dotenv

load_dotenv()

PVE_HOST = os.getenv("PVE_HOST", "192.168.0.50")
PVE_TOKEN_ID = os.getenv("PVE_TOKEN_ID", "")
PVE_TOKEN_SECRET = os.getenv("PVE_TOKEN_SECRET", "")
