import asyncio
from pingbot.utils.blockchain import PingSolanaClient


async def main():
    PingClient = PingSolanaClient()
    info = await PingClient.get_mint_liquidity_pool_address()("92TUnL8sEsSoQfp96cc9vBKV5rdbMn2wZWeXTGdr62zP")
    print(info)

asyncio.run(main())