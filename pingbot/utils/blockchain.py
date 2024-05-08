import asyncio
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey  # type: ignore

from pingbot.utils.enums import ProgramIdType
from pingbot.utils.metadata import unpack_metadata_account

__all__ = ["PingSolanaClient", ]

class PingSolanaClient:
    BASE_RPC_ENDPOINT = "https://api.mainnet-beta.solana.com"

    def __init__(self) -> None:
        self.client = AsyncClient(self.BASE_RPC_ENDPOINT)
        # self.private_client =  AsyncClient("")

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
        return token_info['name'], token_info['symbol']
    
    async def get_mint_liquidity_pool_address(self, mint):
        """
        `get_liquidity_pool_address` retrieves the liquidity pool address for a given mint.

        ##  Parameters
        
            `mint`: (str): public key representing a token mint address
        """
        return await self.get_program_address(mint,ProgramIdType.RAYDIUM_AUTHORITY.value)
        