# config/config.py
import os

# Telegram Bot Token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7826250143:AAGXRLK4kmPTU_Iv2YsgB_72-oHbAUGHhZg")

# Path to the valid keys file
VALID_KEYS_FILE = os.getenv("VALID_KEYS_FILE", "config/keys.json")

# Path to the active sessions file
ACTIVE_SESSIONS_FILE = os.getenv("ACTIVE_SESSIONS_FILE", "config/active_sessions.json")

# Path to the wallets file
WALLETS_FILE = os.getenv("WALLETS_FILE", "config/wallets.json")

# Path to the admin wallets file
ADMIN_WALLETS_FILE = os.getenv("ADMIN_WALLETS_FILE", "config/admin_wallets.json")