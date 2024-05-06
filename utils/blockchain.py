#from django.conf import settings
from solana.rpc.api import Client
from solders.pubkey import Pubkey # type: ignore

class SolanaChain:
    

    def __init__(self,mint, endpoint="https://api.mainnet-beta.solana.com",) -> None:
        self.client = Client(endpoint)
        self.rayduim_endpoint = ""
        self.mint = Pubkey.from_string(mint)
