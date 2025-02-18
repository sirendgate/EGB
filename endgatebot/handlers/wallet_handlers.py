# handlers/wallet_handlers.py
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.wallet_services import WalletService
from utils.file_utils import load_json, save_json
from config.config import WALLETS_FILE, ADMIN_WALLETS_FILE
from utils.navigation import start

# Set up logging
logger = logging.getLogger(__name__)

wallet_service = WalletService()

async def wallet_manager_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display the Wallet Manager menu."""
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("🆕 Generate Wallet", callback_data='generate_wallet')],
        [InlineKeyboardButton("📥 Import Wallet", callback_data='import_wallet')],
        [InlineKeyboardButton("👀 View Wallets", callback_data='view_wallets')],
        [InlineKeyboardButton("🔙 Back", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="💼 Wallet Manager: Choose an option below:", reply_markup=reply_markup)

async def generate_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate a new wallet and display it to the user."""
    query = update.callback_query
    await query.answer()

    # Generate a new wallet
    wallet = wallet_service.generate_wallet()

    # Load admin wallets or initialize if the file doesn't exist
    admin_wallets = load_json(ADMIN_WALLETS_FILE, default={"wallets": []})
    if "wallets" not in admin_wallets:  # Ensure the "wallets" key exists
        admin_wallets["wallets"] = []

    # Save the wallet to the admin_wallets.json file
    admin_wallets["wallets"].append(wallet)
    save_json(ADMIN_WALLETS_FILE, admin_wallets)

    # Display the wallet details to the user with a back button
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Menu", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"✅ Wallet generated successfully:\n\n"
        f"<b>Public Key:</b> <code>{wallet['public_key']}</code>\n"
        f"<b>Private Key:</b> <code>{wallet['private_key']}</code>\n\n"
        "<b>⚠️ Save this information now. It will not be shown again.</b>",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

async def import_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle wallet import by private key."""
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text="📥 Please enter your private key:")
    else:
        private_key = update.message.text.strip()
        if not private_key or len(private_key) != 64:  # Basic validation
            await update.message.reply_text("❌ Invalid private key format.")
            return

        try:
            wallet = wallet_service.import_wallet(private_key)
            await update.message.reply_text(
                f"✅ Wallet imported successfully:\n\n"
                f"<b>Public Key:</b> <code>{wallet['public_key']}</code>\n\n"
                "<b>⚠️ Save your private key securely. It will not be shown again.</b>",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Error importing wallet: {e}")
            await update.message.reply_text(f"❌ Error importing wallet: {str(e)}")

async def view_wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display all wallets with their balances and options."""
    query = update.callback_query
    await query.answer()

    wallets = wallet_service.get_all_wallets()
    if not wallets:
        await query.edit_message_text(text="❌ No wallets found. Generate or import a wallet first.")
        return

    response = "💼 <b>All Wallets</b>:\n\n"
    for i, wallet in enumerate(wallets):
        response += (
            f"🔑 <b>Wallet {i+1}</b>: <code>{wallet['public_key']}</code>\n"
            f"💰 <b>Balance</b>: {wallet.get('balance', '0.0000 SOL ($0.00 USD)')}\n\n"
        )

    # Create buttons for each wallet
    keyboard = []
    for i, wallet in enumerate(wallets):
        keyboard.append([
            InlineKeyboardButton(f"🔘 Set as Active (Wallet {i+1})", callback_data=f'set_active_{i}'),
            InlineKeyboardButton(f"❌ Delete (Wallet {i+1})", callback_data=f'delete_wallet_{i}')
        ])
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='back')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(response, reply_markup=reply_markup, parse_mode="HTML")

async def set_active_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set a wallet as the active wallet."""
    query = update.callback_query
    await query.answer()

    wallet_index = int(query.data.split('_')[-1])
    wallet_service.set_default_wallet(wallet_index)
    await query.edit_message_text(f"✅ Wallet {wallet_index + 1} set as active.")

async def delete_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompt the user to confirm wallet deletion."""
    query = update.callback_query
    await query.answer()

    wallet_index = int(query.data.split('_')[-1])
    context.user_data['wallet_to_delete'] = wallet_index  # Store the wallet index for confirmation

    # Ask for confirmation
    keyboard = [
        [InlineKeyboardButton("✅ Yes", callback_data=f'confirm_delete_{wallet_index}')],
        [InlineKeyboardButton("❌ No", callback_data='cancel_delete')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f"⚠️ Are you sure you want to delete Wallet {wallet_index + 1}?",
        reply_markup=reply_markup
    )

async def confirm_delete_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle wallet deletion confirmation."""
    query = update.callback_query
    await query.answer()

    wallet_index = int(query.data.split('_')[-1])
    wallet_service.delete_wallet(wallet_index)
    await query.edit_message_text(f"✅ Wallet {wallet_index + 1} deleted.")

async def cancel_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle cancellation of wallet deletion."""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text("❌ Deletion canceled.")