import asyncio
from pingbot.utils.blockchain import PingSolanaClient


async def main():
    PingClient = PingSolanaClient()
    info = await PingClient.get_token_info("92TUnL8sEsSoQfp96cc9vBKV5rdbMn2wZWeXTGdr62zP")
    print(info)

asyncio.run(main())