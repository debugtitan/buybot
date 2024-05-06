import time
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update:Update, context, *args, **kwargs):
            await context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id, action=action
            )
            return await func(update, context, *args, **kwargs)

        return command_func

    return decorator


def check_chat_type(func):
    """Decorator to checks chat type"""

    @wraps(func)
    async def command_func(update:Update, context, *args, **kwargs):
        private = False
        if update.effective_chat.type == "private":
            return await func(update, context, private=True)
        return await func(update, context, private=private)

    return command_func



def handler_decorator(func):
    @wraps(func)
    @check_chat_type
    @send_action(ChatAction.TYPING)
    async def wrapper(update, callback, *args, **kwargs):
        await func(update, callback, *args, **kwargs)

    return wrapper


# Plans to accept for multiple token mints and groups
class MWT(object):
    """Memoize With Timeout"""
    _caches = {}
    _timeouts = {}

    def __init__(self,timeout=2):
        self.timeout = timeout

    def collect(self):
        """Clear cache of results which have timed out"""
        for func in self._caches:
            cache = {}
            for key in self._caches[func]:
                if (time.time() - self._caches[func][key][1]) < self._timeouts[func]:
                    cache[key] = self._caches[func][key]
            self._caches[func] = cache

    def __call__(self, f):
        self.cache = self._caches[f] = {}
        self._timeouts[f] = self.timeout

        def func(*args, **kwargs):
            kw = sorted(kwargs.items())
            key = (args, tuple(kw))
            try:
                v = self.cache[key]
                print("cache")
                if (time.time() - v[1]) > self.timeout:
                    raise KeyError
            except KeyError:
                v = self.cache[key] = f(*args,**kwargs),time.time()
            return v[0]
        func.func_name = f.__name__

        return func
    
@MWT(timeout=60*60)
async def get_admin_ids(context:ContextTypes.DEFAULT_TYPE, chat_id:int):
    """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
    return [admin.user.id for admin in await context.bot.get_chat_administrators(chat_id)]