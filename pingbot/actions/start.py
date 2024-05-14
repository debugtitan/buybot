from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from pingbot.resources.models import PingBot
from pingbot.utils import logger,decorators,keyboards

@decorators.handler_decorator
async def start_handler(update:Update, context:ContextTypes.DEFAULT_TYPE, *args, **kwargs):
    """ /start message handler"""
    user = update.effective_message
    _is_chat_type_private = kwargs.get('private') # the decorator handles the private instance
    ping_admin = await PingBot.objects.aget(pk=1)
    if _is_chat_type_private and int(ping_admin.owner) == int(user.chat_id):
        msg = f"Hey {user.from_user.first_name}! 🚀\n\nPingBot helps you effortlessly track all your buys and sells of your tokens on the Solana Blockchain"
        await update.message.reply_text(msg,parse_mode=ParseMode.HTML,reply_markup=keyboards.TOKEN_KEYBOARD_BUTTONS)

    logger.info(f"{user.from_user.first_name} ({user.chat_id}) Private chat: {_is_chat_type_private}")