from django.conf import settings
from pingbot.utils.blockchain import PingSolanaClient


ping = PingSolanaClient(settings.PRIVATE_RPC_CLIENT)