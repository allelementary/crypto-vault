import base64
import json
import os
from typing import Union

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Encryption:
    """
    Encrypt & Decrypt data using AES-256-CBC
    """

    @staticmethod
    def generate_key() -> bytes:
        return os.urandom(32)

    @staticmethod
    def encrypt(data: Union[int, str, list, dict], key: bytes) -> bytes:
        try:
            # Convert the data to JSON and then to bytes
            json_data = json.dumps(data)
            bytes_data = bytes(json_data, "utf-8")

            # Create a padder instance and pad the data
            padder = padding.PKCS7(algorithms.AES.block_size).padder()
            padded_data = padder.update(bytes_data) + padder.finalize()

            # Generate a random IV and create a cipher object
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            encryptor = cipher.encryptor()

            # Encrypt the padded data
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            b64_encrypted_data = base64.b64encode(encrypted_data).decode("utf-8")
            b64_iv = base64.b64encode(iv).decode("utf-8")
            encrypted_data_obj = {"encrypted_data": b64_encrypted_data, "iv": b64_iv}

            return json.dumps(encrypted_data_obj).encode("utf-8")
        except Exception as e:
            raise Exception(f"Error encrypting data: {str(e)}")

    @staticmethod
    def decrypt(data: bytes, key: bytes) -> Union[int, str, list, dict]:
        try:
            # Load the encrypted data object
            data_obj = json.loads(data.decode("utf-8"))
            encrypted_data = base64.b64decode(data_obj.get("encrypted_data"))
            iv = base64.b64decode(data_obj.get("iv"))

            # Create a cipher object
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            decryptor = cipher.decryptor()

            # Decrypt the data
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

            return json.loads(unpadded_data.decode("utf-8"))
        except Exception as e:
            raise Exception(f"Error decrypting data: {str(e)}")
