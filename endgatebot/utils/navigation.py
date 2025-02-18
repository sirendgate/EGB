# utils/navigation.py
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.wallet_services import WalletService
from utils.file_utils import load_json, save_json
from config.config import ACTIVE_SESSIONS_FILE

# Set up logging
logger = logging.getLogger(__name__)

wallet_service = WalletService()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display the main menu."""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        chat_id = query.message.chat_id
        message_id = query.message.message_id
    else:
        chat_id = update.message.chat_id
        message_id = None

    user_id = update.message.from_user.id
    logger.debug(f"User {user_id} attempted to start the bot.")

    # Load active sessions
    active_sessions = load_json(ACTIVE_SESSIONS_FILE, default={"active_sessions": {}})
    logger.debug(f"Active sessions: {active_sessions}")

    # Check if the user is in active sessions
    if str(user_id) not in active_sessions.get("active_sessions", {}):
        logger.warning(f"User {user_id} is not in active sessions.")
        await context.bot.send_message(chat_id=chat_id, text="❌ Please unlock the bot by entering your key.")
        return

    logger.debug(f"User {user_id} is in active sessions. Proceeding to main menu.")

    # Fetch the current wallet and balance
    current_wallet = wallet_service.get_default_wallet()
    balance = current_wallet.get('balance', '0.0000 SOL ($0.00 USD)') if current_wallet else "0.0000 SOL ($0.00 USD)"

    # Get the user's first name
    user_name = update.message.from_user.first_name

    # Display the dashboard
    if current_wallet:
        response = (
            f"🚀 <b>Welcome, {user_name}!</b>\n\n"
            f"💼 <b>Current Wallet</b>: <code>{current_wallet['public_key']}</code>\n"
            f"💰 <b>Balance</b>: {balance}\n\n"
            "To get started, simply press the <b>Launch</b> button.\n"
            "Need help? Check out our beginner guide available on our <a href='https://discord.gg/AegGGVV4dK'>Discord</a>.\n\n"
            "Please choose an option:"
        )
    else:
        response = (
            f"🚀 <b>Welcome, {user_name}!</b>\n\n"
            "💼 <b>Current Wallet</b>: None\n"
            "💰 <b>Balance</b>: 0.0000 SOL ($0.00 USD)\n\n"
            "To get started, simply press the <b>Launch</b> button.\n"
            "Need help? Check out our beginner guide available on our <a href='https://discord.gg/AegGGVV4dK'>Discord</a>.\n\n"
            "Please choose an option:"
        )

    # Updated dashboard layout
    keyboard = [
        [InlineKeyboardButton("🚀 Launch", callback_data='launch')],  # Main button
        [  # Second row: Settings and Wallet Manager
            InlineKeyboardButton("⚙️ Settings", callback_data='settings'),
            InlineKeyboardButton("💼 Wallet Manager", callback_data='wallet_manager')
        ],
        [  # Third row: Volume Tools and Comment Bot
            InlineKeyboardButton("📊 Volume Tools", callback_data='volume_tools'),
            InlineKeyboardButton("💬 Comment Bot", callback_data='comment_bot')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if message_id:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=response, reply_markup=reply_markup, parse_mode="HTML")
    else:
        await context.bot.send_message(chat_id=chat_id, text=response, reply_markup=reply_markup, parse_mode="HTML")