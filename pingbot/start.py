import os, django,telegram
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from django.conf import settings
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.error import InvalidToken
from resources.models import PingBot
from pingbot.actions import start_handler
from pingbot.utils import logger


class SolanaPingBot:
    """ Solana Ping """

    def __init__(self):
        self.ptb = Application.builder().token(self._get_token()).build()
        self._register_handlers()

    def _get_token(self):
        """ get bot token from environ"""
        if settings.TOKEN is not None:
            return settings.TOKEN
        logger.error("key 'TOKEN' not set in .env file")
        exit()

    def _register_handlers(self):
        """ add all handlers (command handler, callbackquery handlers, message handlers)"""
        self.ptb.add_handler(CommandHandler("start",start_handler))

        
    
    def start(self):
        """ Start up telegram bot polling"""
        # Create Ping Config instance if not exist
        PingBot.objects.get_or_create(pk=1)
        try:
            logger.info("Application startup!")
            self.ptb.run_polling()
        except InvalidToken:
            logger.error("You must pass the token you received from https://t.me/Botfather!")
            exit()