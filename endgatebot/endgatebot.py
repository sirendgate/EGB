# endgatebot.py
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from handlers.auth_handlers import unlock_bot
from handlers.wallet_handlers import wallet_manager_menu, generate_wallet, import_wallet, view_wallets, set_active_wallet, delete_wallet, confirm_delete_wallet, cancel_delete
from handlers.menu_handlers import button
from handlers.volume_handlers import auto_volume, handle_microbuys, handle_bumps, process_volume_input
from handlers.bundle_handlers import handle_bundle, process_bundle_input
from handlers.launch_handlers import launch_coin, process_coin_details
from handlers.comment_handlers import comment_bot, process_comment_input  # Correct import
from config.config import TOKEN
from utils.logging_utils import setup_logging
from utils.navigation import start

# Enable logging
setup_logging()

def main():
    # Initialize the bot
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))  # /start command
    application.add_handler(CallbackQueryHandler(button))  # Handle button presses
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unlock_bot))  # Handle unlock key input

    # Wallet Manager handlers
    application.add_handler(CallbackQueryHandler(wallet_manager_menu, pattern='^wallet_manager$'))  # Wallet Manager menu
    application.add_handler(CallbackQueryHandler(generate_wallet, pattern='^generate_wallet$'))  # Generate Wallet
    application.add_handler(CallbackQueryHandler(import_wallet, pattern='^import_wallet$'))  # Import Wallet
    application.add_handler(CallbackQueryHandler(view_wallets, pattern='^view_wallets$'))  # View Wallets
    application.add_handler(CallbackQueryHandler(set_active_wallet, pattern='^set_active_'))  # Set Active Wallet
    application.add_handler(CallbackQueryHandler(delete_wallet, pattern='^delete_wallet_'))  # Delete Wallet
    application.add_handler(CallbackQueryHandler(confirm_delete_wallet, pattern='^confirm_delete_'))  # Confirm Delete
    application.add_handler(CallbackQueryHandler(cancel_delete, pattern='^cancel_delete$'))  # Cancel Delete
    application.add_handler(CallbackQueryHandler(start, pattern='^back$'))  # Back Button

    # Volume Tools handlers
    application.add_handler(CallbackQueryHandler(auto_volume, pattern='^auto_volume$'))  # Automated Volume
    application.add_handler(CallbackQueryHandler(handle_microbuys, pattern='^microbuys$'))  # Microbuys
    application.add_handler(CallbackQueryHandler(handle_bumps, pattern='^bumps$'))  # Bumps
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_volume_input))  # Volume input handler

    # Bundle handler
    application.add_handler(CallbackQueryHandler(handle_bundle, pattern='^bundle$'))  # Bundle command
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_bundle_input))  # Bundle input handler

    # Launch Coin handler
    application.add_handler(CallbackQueryHandler(launch_coin, pattern='^launch_coin$'))  # Launch Coin
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_coin_details))  # Coin details handler

    # Comment Bot handler
    application.add_handler(CallbackQueryHandler(comment_bot, pattern='^comment_bot$'))  # Comment Bot
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_comment_input))  # Comment input handler

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()