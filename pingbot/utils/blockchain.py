import time,os
from typing import List, Union
from solana.rpc.async_api import AsyncClient
from solana.rpc.types import MemcmpOpts
from solana.rpc.websocket_api import connect
from solders.signature import Signature # type: ignore
from solders.pubkey import Pubkey  # type: ignore
from solders.rpc.config import RpcTransactionLogsFilterMentions # type: ignore
from websockets.exceptions import ConnectionClosedError
from pingbot.utils.enums import ProgramIdType
from pingbot.utils.metadata import (
    calculate_asset_value,
    format_number,
    unpack_metadata_account
)
from pingbot.utils.enums import MarketType
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()


__all__ = [
    "PingSolanaClient",
]

async def listen_to_event(amm_pool):
    from django.conf import settings
    """"""
    async with connect("wss://api.mainnet-beta.solana.com") as websocket:
        await websocket.logs_subscribe(
                RpcTransactionLogsFilterMentions(Pubkey.from_string(str(amm_pool))),
                commitment="finalized",
            )
        while True:
            try:
                    data = await websocket.recv()
                    print(data)
                    _result = data[0].result
                    if hasattr(_result, "value"):
                        result = _result.value
                        log_signature, logs = result.signature, result.logs
                        if any("Program log: Instruction: Transfer" in log for log in logs):
                            client = PingSolanaClient(settings.PRIVATE_RPC_CLIENT)
                            await client.get_transaction_info(log_signature)
                        
            except ConnectionClosedError as e:
                time.sleep(20)
                await listen_to_event(amm_pool)
            except KeyboardInterrupt:
                exit()

class PingSolanaClient:
    
    BASE_RPC_ENDPOINT = "https://api.mainnet-beta.solana.com"

    def __init__(self, endpoint=None) -> None:
        self.client = (
            AsyncClient(endpoint) if endpoint else AsyncClient(self.BASE_RPC_ENDPOINT)
        )

    async def get_account_info(self, account):
        """
        `get_account_info`: get account information for specific account

        Parameters

        ##  Required:
                - `account` (str): account to fetch information
        """
        account_instance = await self.client.get_account_info_json_parsed(
            Pubkey.from_string(str(account))
        )
        return account_instance.value.data

    async def get_program_address(
        self, mint, program_id=ProgramIdType.META_DATA_PROGRAM.value
    ):
        """
        `get_program_address`: get associated program account for a mint.

        Parameters

        ##  Required:
                - `mint` (str): token mint which you want to retrieve the associated program account.
                - `program_id` (str): program ID associated with the mint for which you want to retrieve the program account.
        """
        return Pubkey.find_program_address(
            [
                b"metadata",
                bytes(Pubkey.from_string(str(program_id))),
                bytes(Pubkey.from_string(str(mint))),
            ],
            Pubkey.from_string(str(program_id)),
        )[0]

    async def fetch_mint_pool_amm_id(self, mint):
        """
        `get_liquidity_pool_address` retrieves the liquidity pool address for a given mint.

        ##  Parameters

            `mint`: (str): public key representing a token mint address
        """
        memcmp_opts_1 = MemcmpOpts(offset=400, bytes=str(mint))
        memcmp_opts_2 = MemcmpOpts(
            offset=432, bytes=str(ProgramIdType.WRAPPED_SOL.value)
        )
        filters: List[Union[int, MemcmpOpts]] = [752, memcmp_opts_1, memcmp_opts_2]
        resp = await self.client.get_program_accounts(
            Pubkey.from_string(str(ProgramIdType.RAYDIUM_POOL.value)),
            encoding="base64",
            filters=filters,
        )
        return resp.value[0].pubkey
    
    async def get_token_supply(self, mint):
        """
        retrieves mint circulating supply

        ##  required
                - `mint` (str): token mint
        """
        _supply = await self.client.get_token_supply(Pubkey.from_string(str(mint)))
        return _supply.value.ui_amount

    async def get_token_info(self, mint):
        """
        retrieves token information by unpacking metadata from an account
        associated with a given mint.

        ##  Required:
                - `mint` (str): token mint which you want to retrieve the meta-data account info.
        """
        program_address = await self.get_program_address(str(mint))
        account_info_instance = await self.get_account_info(program_address)
        token_info = await unpack_metadata_account(account_info_instance)
        return token_info["name"], token_info["symbol"]
    
    async def get_transaction_info(self, signature):
        from pingbot.resources.models import PingBot
        """
        `get_transaction_info` is returning the metadata of a transaction identified by the given signature.

        ## Required 
            - `signature` (str): transaction signature
        """
        tx_signature = Signature.from_string(str(signature))
        tx_info  = await self.client.get_transaction(tx_signature,"jsonParsed",max_supported_transaction_version=0)
        data = tx_info.value.transaction.meta
        post_token_balance = [item for item in data.post_token_balances if str(item.owner) == str(ProgramIdType.RAYDIUM_AUTHORITY.value)]
        pre_token_balance = [item for item in data.pre_token_balances if str(item.owner) == str(ProgramIdType.RAYDIUM_AUTHORITY.value)]
        token_a_base = post_token_balance[0]#
        token_a_quote = post_token_balance[1]
        token_b_base = pre_token_balance[0]
        token_b_quote = pre_token_balance[1]
        ORDER = None
        GOT = None
        SPENT = None
        PRICE = None
        MSG = None
        
        liquidity = post_token_balance[1].ui_token_amount.ui_amount

        if token_a_base.mint == token_b_base.mint:
            ORDER = MarketType.SOLD.value if token_a_base.ui_token_amount.ui_amount > token_b_base.ui_token_amount.ui_amount else MarketType.BUY.value
        if ORDER == MarketType.BUY.value:
            SPENT = token_a_quote.ui_token_amount.ui_amount - token_b_quote.ui_token_amount.ui_amount
            GOT = token_b_base.ui_token_amount.ui_amount - token_a_base.ui_token_amount.ui_amount
            PRICE = post_token_balance[1].ui_token_amount.ui_amount / post_token_balance[0].ui_token_amount.ui_amount
        else:
            SPENT = token_b_quote.ui_token_amount.ui_amount - token_a_quote.ui_token_amount.ui_amount
            GOT = token_a_base.ui_token_amount.ui_amount - token_b_base.ui_token_amount.ui_amount
            PRICE = post_token_balance[1].ui_token_amount.ui_amount / post_token_balance[0].ui_token_amount.ui_amount

        token_info = await PingBot.objects.aget(pk=1)
        price_usd = calculate_asset_value(PRICE)
        MCAP = token_info.mint_supply * price_usd
        POOL= calculate_asset_value(liquidity)
        spent_usd = calculate_asset_value(SPENT)
        if ORDER == MarketType.BUY.value:
            MSG = f"<b>{token_info.mint_name} Buy!</b>\n\n∴ Spent: {format_number(SPENT,8)} SOL (${format_number(spent_usd,4)})\n↳ Got: {format_number(GOT)} {token_info.mint_symbol}\n\nPrice: {format_number(PRICE)} WSOL (${format_number(price_usd)})\n"\
                  f"💰 MarketCap: ${format_number(MCAP)}\n💧Liquidity: {format_number(liquidity,6)} WSOL (${format_number(POOL,6)})\n\n" \
                  f"<a href='https://raydium.io/swap/?inputCurrency=sol&outputCurrency={token_info.token_mint}'>Buy</a> <a href='https://birdeye.so/token/{token_info.token_mint}'>Chart</a>"
        else:
            MSG = f"<b>{token_info.mint_name} Sell!</b>\n⌞Sold: {format_number(GOT)} {token_info.mint_symbol}\n∴ For: {format_number(SPENT,8)} SOL (${format_number(spent_usd,4)})\n\nPrice: {format_number(PRICE)} WSOL (${format_number(price_usd)})\n"\
                  f"💰 MarketCap: ${format_number(MCAP)}\n💧Liquidity: {format_number(liquidity,6)} WSOL (${format_number(POOL,6)})\n\n" \
                  f"<a href='https://raydium.io/swap/?inputCurrency=sol&outputCurrency={token_info.token_mint}'>Buy</a> <a href='https://birdeye.so/token/{token_info.token_mint}'>Chart</a>"

    
