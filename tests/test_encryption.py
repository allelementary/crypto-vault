import pytest

from crypto_vault.crypto_vault import Encryption


def test_generate_key():
    """
    Test 256 bits encryption key generation, ensure size
    """
    key = Encryption.generate_key()
    assert len(key) == 32


def test_unique_key():
    """
    Test 256 bits encryption key generation, ensure uniqueness
    """
    key1 = Encryption.generate_key()
    key2 = Encryption.generate_key()
    assert key1 != key2


@pytest.mark.parametrize("data", ["Hello world!", 42, [1, 2, 3], {"key": "value"}])
def test_encrypt_decrypt(data):
    """
    Test encryption and decryption
    """
    key = Encryption.generate_key()
    encrypted_data = Encryption.encrypt(data, key)
    decrypted_data = Encryption.decrypt(encrypted_data, key)
    assert data == decrypted_data


def test_cant_decrypt_with_wrong_key():
    """
    Test decryption with wrong key
    """
    key1 = Encryption.generate_key()
    key2 = Encryption.generate_key()
    data = "Hello world!"
    encrypted_data = Encryption.encrypt(data, key1)
    with pytest.raises(Exception):
        Encryption.decrypt(encrypted_data, key2)
