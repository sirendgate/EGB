# handlers/auth_handlers.py
import json
import logging
from telegram import Update
from telegram.ext import ContextTypes
from utils.file_utils import load_json, save_json
from config.config import VALID_KEYS_FILE, ACTIVE_SESSIONS_FILE
from utils.navigation import start

# Set up logging
logger = logging.getLogger(__name__)

async def unlock_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unlock the bot if the user provides a valid key."""
    user_id = update.message.from_user.id
    user_key = update.message.text.strip()

    logger.debug(f"User {user_id} entered key: {user_key}")

    # Load valid keys
    keys_data = load_json(VALID_KEYS_FILE, default={"valid_keys": []})
    logger.debug(f"Loaded keys data: {keys_data}")

    valid_keys = keys_data.get("valid_keys", [])
    logger.debug(f"Valid keys: {valid_keys}")

    if not isinstance(valid_keys, list):
        logger.error("Error: 'valid_keys' is not a list! Check your keys.json file.")
        await update.message.reply_text("❌ Internal error. Please contact support.")
        return

    if user_key in valid_keys:
        logger.debug(f"Key {user_key} is valid.")

        # Load active sessions
        active_sessions = load_json(ACTIVE_SESSIONS_FILE, default={"active_sessions": {}})
        logger.debug(f"Loaded active sessions: {active_sessions}")

        if not isinstance(active_sessions, dict) or "active_sessions" not in active_sessions:
            logger.error("Error: 'active_sessions' is not properly structured! Check your JSON file.")
            await update.message.reply_text("❌ Internal error. Please contact support.")
            return

        # Add user to active sessions
        active_sessions["active_sessions"][str(user_id)] = True
        save_json(ACTIVE_SESSIONS_FILE, active_sessions)
        logger.debug(f"Updated active sessions: {active_sessions}")

        # Remove used key from the list
        valid_keys.remove(user_key)
        save_json(VALID_KEYS_FILE, {"valid_keys": valid_keys})
        logger.debug(f"Updated valid keys after removal: {valid_keys}")

        await update.message.reply_text("✅ Bot unlocked! Use /start to begin.")
    else:
        logger.warning(f"Invalid key entered: {user_key}")
        await update.message.reply_text("❌ Invalid key. Please try again.")