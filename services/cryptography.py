from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend

def encrypt_by_chacha20(plaintext: bytes, key: bytes, nonce: bytes) -> bytes:
    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext)

    return ciphertext

def decrypt_by_chacha20(ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    decryptor = cipher.decryptor()

    plaintext = decryptor.update(ciphertext)

    return plaintext