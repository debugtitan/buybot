import logging
from telegram.ext import Application
from django.conf import settings
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
# If you don't do this, others can seeyour bot token if on public server
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


ptb = Application.builder().token(settings.TOKEN).build()