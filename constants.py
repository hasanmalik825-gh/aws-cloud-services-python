import os
from pathlib import Path

# AWS
AWS_ACCESS_KEY_ID = os.getenv("MYACCESSKEY")
AWS_SECRET_ACCESS_KEY = os.getenv("MYSECRETKEY")
AWS_REGION = os.getenv("AWS_REGION") or "us-east-1"

# IP Whitelist
IP_WHITELIST = os.getenv("IP_WHITELIST") or ["127.0.0.1"]

IMAGES_DIR = Path("static/images")
PORT = os.getenv("PORT") or 8000
BASE_URL = f"http://localhost:{PORT}"


