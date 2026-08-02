import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY is not set in .env")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Data Files
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
SUMMARY_FILE = os.path.join(DATA_DIR, "summary.json")
SESSION_FILE = os.path.join(DATA_DIR, "session.json")
MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")

# Limits
MAX_HISTORY_TOKENS = int(os.getenv("MAX_HISTORY_TOKENS", 4000))
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", 50))
