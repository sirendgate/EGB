# handlers/comment_handlers.py
import logging
from telegram import Update
from telegram.ext import ContextTypes

# Set up logging
logger = logging.getLogger(__name__)

async def comment_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle comment bot functionality."""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "💬 Comment Bot: Enter the transaction hash and your comment:\n\n"
        "<b>TransactionHash Comment</b>\n\n"
        "Example: 5n7L... Hello, this is a test comment!"
    )
    context.user_data['awaiting_comment_input'] = True

async def process_comment_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process user input for posting a comment."""
    user_input = update.message.text.strip()
    try:
        transaction_hash, comment = user_input.split(maxsplit=1)

        # Post the comment (placeholder for now)
        await update.message.reply_text(
            f"✅ Comment posted on transaction <code>{transaction_hash}</code>:\n\n"
            f"{comment}",
            parse_mode="HTML"
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid input format. Please use: TransactionHash Comment")
    except Exception as e:
        await update.message.reply_text(f"❌ An error occurred: {e}")