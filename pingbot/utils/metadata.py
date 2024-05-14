# https://github.com/metaplex-foundation/python-api/blob/main/metaplex/metadata.py

import struct
import base58
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

def format_number(number, points:int=10):
    if abs(number) >= 1e15:
        return f"{number / 1e15:.2f}Q"
    elif abs(number) >= 1e12:
        return f"{number / 1e12:.2f}T"
    elif abs(number) >= 1e9:
        return f"{number / 1e9:.2f}B"
    elif abs(number) >= 1e6:
        return f"{number / 1e6:.2f}M"
    elif abs(number) >= 1e3:
        return f"{number / 1e3:.2f}K"
    elif number < 1000:
        return f"{number:.2f}"
    elif number < 1:
        return f"{number:.{points}f}"



        
def calculate_asset_value(amount):
    price_per_sol = cg.get_price("solana", "usd")["solana"]["usd"]
    return amount * price_per_sol

def truncate_address(address):
    if len(address) <= 14:
        return address
    else:
        prefix = address[:6]
        suffix = address[-6:]
        dots = "*" * 5
        return prefix + dots + suffix
    
async def unpack_metadata_account(data):
    assert data[0] == 4
    i = 1
    source_account = base58.b58encode(
        bytes(struct.unpack("<" + "B" * 32, data[i : i + 32]))
    )
    i += 32
    mint_account = base58.b58encode(
        bytes(struct.unpack("<" + "B" * 32, data[i : i + 32]))
    )
    i += 32
    name_len = struct.unpack("<I", data[i : i + 4])[0]
    i += 4
    name = struct.unpack("<" + "B" * name_len, data[i : i + name_len])
    i += name_len
    symbol_len = struct.unpack("<I", data[i : i + 4])[0]
    i += 4
    symbol = struct.unpack("<" + "B" * symbol_len, data[i : i + symbol_len])
    i += symbol_len
    uri_len = struct.unpack("<I", data[i : i + 4])[0]
    i += 4
    uri = struct.unpack("<" + "B" * uri_len, data[i : i + uri_len])
    i += uri_len
    fee = struct.unpack("<h", data[i : i + 2])[0]
    i += 2
    has_creator = data[i]
    i += 1
    creators = []
    verified = []
    share = []
    if has_creator:
        creator_len = struct.unpack("<I", data[i : i + 4])[0]
        i += 4
        for _ in range(creator_len):
            creator = base58.b58encode(
                bytes(struct.unpack("<" + "B" * 32, data[i : i + 32]))
            )
            creators.append(creator)
            i += 32
            verified.append(data[i])
            i += 1
            share.append(data[i])
            i += 1
    primary_sale_happened = bool(data[i])
    i += 1
    is_mutable = bool(data[i])
    metadata = {
        "update_authority": source_account,
        "mint": mint_account,
        "data": {
            "name": bytes(name).decode("utf-8").strip("\x00"),
            "symbol": bytes(symbol).decode("utf-8").strip("\x00"),
            "uri": bytes(uri).decode("utf-8").strip("\x00"),
            "seller_fee_basis_points": fee,
            "creators": creators,
            "verified": verified,
            "share": share,
        },
        "primary_sale_happened": primary_sale_happened,
        "is_mutable": is_mutable,
    }
    return metadata["data"]

