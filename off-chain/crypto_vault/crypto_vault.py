import json
import os
from typing import Optional

from eth_typing import Address
from web3 import Web3

from crypto_vault.config import settings
from crypto_vault.encryption import Encryption


class CryptoVault(Encryption):
    """
    Store, update and retrieve on-chain data,
    including encryption, decryption and sending blockchain transactions
    """
    contract_address: Address = settings.CONTRACT_ADDRESS

    def __init__(
        self, app: str, env: str, private_key: str, encryption_key: bytes, http_provider: str
    ) -> None:
        self.app = app
        self.env = env
        self.private_key = private_key
        self.encryption_key = encryption_key
        self.w3 = Web3(Web3.HTTPProvider(http_provider))

    @property
    def abi(self):
        filename = settings.ABI_FILENAME
        current_dir = os.path.dirname(__file__)
        path = os.path.join(current_dir, filename)
        with open(path, "r") as file:
            abi = file.read()
        return json.loads(abi).get("abi")

    @property
    def user_address(self):
        return self.w3.eth.account.from_key(self.private_key).address

    def store(self, data: dict):
        # Get and decrypt existing data
        contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)
        encrypted_data = self.encrypt(data=data, key=self.encryption_key)

        # Create a transaction
        tx = contract.functions.store(
            self.w3.to_hex(text=self.app),
            self.w3.to_hex(text=self.env),
            self.w3.to_hex(encrypted_data)
        ).build_transaction(
            {
                "from": self.user_address,
                "nonce": self.w3.eth.get_transaction_count(self.user_address),
                "gasPrice": self.w3.eth.gas_price,
            }
        )

        # Sign and send the transaction
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        return tx_hash.hex()

    def retrieve(self, value_name: Optional[str] = None) -> dict:
        """Retrieve decrypted data from the storage"""
        # Instantiate the contract
        contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)

        # Retrieve the encrypted data from the blockchain
        encrypted_data = contract.functions.retrieve(
            self.w3.to_hex(text=self.app), self.w3.to_hex(text=self.env)
        ).call({"from": self.user_address})

        # Decrypt the data
        decrypted_data = self.decrypt(data=encrypted_data, key=self.encryption_key)
        if value_name:
            return decrypted_data.get(value_name)
        return decrypted_data

    def update(self, data: dict):
        # Get and decrypt existing data
        contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)
        existing_data = contract.functions.retrieve(
            self.w3.to_hex(text=self.app), self.w3.to_hex(text=self.env)
        ).call(
            {"from": self.user_address}
        )
        if existing_data:
            existing_data = self.decrypt(data=existing_data, key=self.encryption_key)
        else:
            existing_data = {}

        # Update and encrypt the data
        existing_data.update(data)
        encrypted_data = self.encrypt(data=existing_data, key=self.encryption_key)

        # Prepare the transaction to store the combined data
        tx_data = {
            "from": self.user_address,
            "nonce": self.w3.eth.get_transaction_count(self.user_address),
            "gasPrice": self.w3.eth.gas_price,
        }
        tx = contract.functions.store(
            self.w3.to_hex(text=self.app), self.w3.to_hex(text=self.env), self.w3.to_hex(encrypted_data)
        ).build_transaction(tx_data)

        # Sign and send the transaction
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        return tx_hash.hex()
