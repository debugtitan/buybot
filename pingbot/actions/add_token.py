from telegram import Update
from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)
from telegram.constants import ParseMode
from pingbot.utils.blockchain import PingSolanaClient
from pingbot.utils import logger
ping = PingSolanaClient()
MINT = range(1)


# Add New Token
async def add_token_inline_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """add token inline query handler"""
    query = update.callback_query
    await query.edit_message_text(
        "Please send *(Token mint)* address for tracking", parse_mode=ParseMode.MARKDOWN
    )
    return MINT


async def get_mint_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """receives user's mint address"""
    _contract_address = update.message.text
    try:
        token_info =  await ping.get_token_info(_contract_address)
        print(token_info)
    except Exception as err:
        logger.error(err)





async def cancel(update:Update, context:ContextTypes.DEFAULT_TYPE):
    """ cancel conversational handler"""
    await update.callback_query.edit_message_text("Operation cancelled. Please use '/start' to restart the process.",parse_mode=ParseMode.MARKDOWN)


token_mint_conv_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(add_token_inline_callback, pattern="add_token#")
    ],
    states={MINT: [MessageHandler(filters.TEXT, get_mint_address)]},
    fallbacks=[CallbackQueryHandler(cancel, pattern="close_process#")],
)
