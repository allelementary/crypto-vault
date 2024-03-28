from pydantic import BaseModel
from eth_typing import Address


class Settings(BaseModel):
    CONTRACT_ADDRESS: Address = "0x276c89d95300b11b8ACEAE24a2dbc4bc3BaB69F5"
    ABI_FILENAME: str = "abi.json"


settings = Settings()
