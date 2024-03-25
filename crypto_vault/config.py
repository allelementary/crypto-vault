from pydantic import BaseModel
from eth_typing import Address


class Settings(BaseModel):
    CONTRACT_ADDRESS: Address = "0x1404951233eCE16010D728F67C8F9b7D8B40fB0e"
    ABI_FILENAME: str = "abi.json"


settings = Settings()
