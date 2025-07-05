import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

LOG_URL = "http://20.244.56.144/evaluation-service/logs"
AUTH_TOKEN = os.getenv("LOG_AUTH_TOKEN") 

def log(message, level="error", package="handler", stack="backend"):
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "stack": stack,
        "level": level,
        "package": package,
        "message": message
    }
    try:
        response = requests.post(LOG_URL, json=data, headers=headers, timeout=3)
        print(f"Log response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Logging failed: {e}")
