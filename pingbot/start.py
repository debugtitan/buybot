import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from django.conf import settings
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram.error import InvalidToken
from pingbot.resources.models import PingBot
from pingbot.actions import start, add_token, token_handler, admin_conv
from pingbot.utils import logger, helpers
from pingbot.utils.decorators import threaded


class SolanaPingBot:
    """Solana Ping"""

    def __init__(self):
        self.ptb = Application.builder().token(self._get_token()).build()
        self._register_handlers()

    def _get_token(self):
        """get bot token from environ"""
        if settings.TOKEN is not None:
            return settings.TOKEN
        logger.error("key 'TOKEN' not set in .env file")
        exit()

    def _register_handlers(self):
        """add all handlers (command handler, callbackquery handlers, message handlers)"""
        self.ptb.add_handler(CommandHandler("start", start.start_handler))
        self.ptb.add_handler(
            CallbackQueryHandler(
                token_handler.check_token_handler, pattern="token_settings#"
            )
        )
        self.ptb.add_handler(
            CallbackQueryHandler(
                admin_conv.remove_mint_from_db, pattern="delete_mint#"
            ),
        )
        self.ptb.add_handler(add_token.token_mint_conv_handler)
        self.ptb.add_handler(admin_conv.admin_conv_handler)

    @threaded
    def run_event_listener(self):
        starter = helpers.PingProcessStarter()
        starter.run()

    def start(self):
        """Start up telegram bot polling"""
        # Create Ping Config instance if not exist
        ping, _ping = PingBot.objects.get_or_create(pk=1)
        
        try:
            logger.info("Application startup!")
            self.run_event_listener()
            self.ptb.run_polling()
            
        except InvalidToken:
            logger.error(
                "You must pass the token you received from https://t.me/Botfather!"
            )
            exit()
        except KeyboardInterrupt:
            exit("CTRL+C ending programe")
