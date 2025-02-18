# handlers/menu_handlers.py
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.navigation import start
from handlers.wallet_handlers import wallet_manager_menu
from handlers.comment_handlers import comment_bot  # Correct import
from services.wallet_services import WalletService

# Set up logging
logger = logging.getLogger(__name__)

wallet_service = WalletService()

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses."""
    query = update.callback_query
    await query.answer()

    if query.data == 'launch':
        keyboard = [
            [InlineKeyboardButton("📦 Bundle", callback_data='bundle')],
            [InlineKeyboardButton("🚀 Launch Coin", callback_data='launch_coin')],
            [InlineKeyboardButton("🔙 Back", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="🚀 Launch: Choose an option below:", reply_markup=reply_markup)
    elif query.data == 'volume_tools':
        keyboard = [
            [InlineKeyboardButton("🤖 Automated Volume", callback_data='auto_volume')],
            [InlineKeyboardButton("🛒 Microbuys", callback_data='microbuys')],
            [InlineKeyboardButton("🚀 Bumps", callback_data='bumps')],
            [InlineKeyboardButton("🔙 Back", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="📊 Volume Tools: Choose an option below:", reply_markup=reply_markup)
    elif query.data == 'wallet_manager':
        await wallet_manager_menu(update, context)
    elif query.data == 'bundle':
        await query.edit_message_text(text="📦 Bundle: Feature under development.")
    elif query.data == 'comment_bot':
        await comment_bot(update, context)  # Call the comment bot handler
    elif query.data == 'settings':
        keyboard = [
            [InlineKeyboardButton("⚙️ Change Default Wallet", callback_data='change_wallet')],
            [InlineKeyboardButton("⚙️ Set Transaction Fee", callback_data='set_fee')],
            [InlineKeyboardButton("🔙 Back", callback_data='back')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="⚙️ Settings: Choose an option below:", reply_markup=reply_markup)
    elif query.data == 'launch_coin':
        await query.edit_message_text(
            "🚀 Launch Coin: Enter the token details in the following format:\n\n"
            "<b>Name Symbol Decimals InitialSupply</b>\n\n"
            "Example: MyToken MTK 9 1000000"
        )
        context.user_data['awaiting_coin_details'] = True
    elif query.data == 'back':
        await start(update, context)
    else:
        await query.edit_message_text(text="❌ Invalid option selected.")

async def process_coin_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the token details and deploy the token."""
    user_input = update.message.text.strip()
    try:
        name, symbol, decimals, initial_supply = user_input.split()
        decimals = int(decimals)
        initial_supply = int(initial_supply)

        # Get the active wallet's private key
        active_wallet = wallet_service.get_default_wallet()
        if not active_wallet:
            await update.message.reply_text("❌ No active wallet found.")
            return

        payer_private_key = active_wallet['private_key']

        # Deploy the token
        token_address = create_token(payer_private_key, name, symbol, decimals, initial_supply)

        await update.message.reply_text(
            f"✅ Token launched successfully!\n\n"
            f"<b>Name:</b> {name}\n"
            f"<b>Symbol:</b> {symbol}\n"
            f"<b>Decimals:</b> {decimals}\n"
            f"<b>Initial Supply:</b> {initial_supply}\n"
            f"<b>Token Address:</b> <code>{token_address}</code>",
            parse_mode="HTML"
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid input format. Please use: Name Symbol Decimals InitialSupply")
    except Exception as e:
        await update.message.reply_text(f"❌ An error occurred: {e}")