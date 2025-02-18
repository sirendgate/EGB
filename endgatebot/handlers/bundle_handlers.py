# handlers/bundle_handlers.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.wallet_services import WalletService
from utils.navigation import start

wallet_service = WalletService()

async def handle_bundle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle bundle distribution."""
    query = update.callback_query
    await query.answer()

    # Get the active wallet
    active_wallet = wallet_service.get_default_wallet()
    if not active_wallet:
        await query.edit_message_text(text="❌ No active wallet found. Please set one in Wallet Manager.")
        return

    # Prompt the user for input
    await query.edit_message_text(text="📦 Enter the total amount of SOL and the number of wallets (e.g., '10 5'):")

    # Wait for user input
    context.user_data['awaiting_bundle_input'] = True

async def process_bundle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process user input for bundle distribution."""
    user_input = update.message.text
    try:
        total_amount, num_wallets = map(float, user_input.split())
        num_wallets = int(num_wallets)
        if total_amount <= 0 or num_wallets <= 0:
            await update.message.reply_text("❌ Amount and number of wallets must be positive.")
            return
        if num_wallets > 20:
            await update.message.reply_text("❌ Maximum of 20 wallets allowed.")
            return

        # Generate wallets if needed
        if len(wallet_service.wallets) < num_wallets:
            for _ in range(num_wallets - len(wallet_service.wallets)):
                wallet_service.generate_wallet()

        # Distribute tokens
        distribution = wallet_service.distribute_tokens(total_amount, num_wallets)
        response = "✅ Tokens distributed:\n"
        for i, amount in enumerate(distribution):
            response += f"Wallet {i+1}: {amount} SOL\n"

        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(response, reply_markup=reply_markup)

    except ValueError:
        await update.message.reply_text("❌ Invalid input format. Please enter numbers (e.g., '100 5').")
    except Exception as e:
        await update.message.reply_text(f"❌ An unexpected error occurred: {e}")