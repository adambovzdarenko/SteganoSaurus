from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import secrets
from argon2.low_level import hash_secret_raw, Type

#CONST
SALT = b"SteganoSaurus-v2" #CHANGE IF YOU WANT TO USE THIS CODE | 16 symbols is optimal
#8+ symbols is needed. Comment this part out if you want to use <16 symbols.
if len(SALT) != 16:
    raise ValueError(f"SALT must be exactly 16 bytes, got {len(SALT)}")

TIME_COST = 3
MEMORY_COST = 65536          # 64 MB
PARALLELISM = 1

def derive_key(passphrase: str) -> bytes:
    return hash_secret_raw(
        secret=passphrase.encode("utf-8"),
        salt=SALT,
        time_cost=TIME_COST,
        memory_cost=MEMORY_COST,
        parallelism=PARALLELISM,
        hash_len=32,
        type=Type.ID,          # Hybrid
    )

#encode the text into the key
def encrypt(text: bytes, passphrase: str) -> bytes:
    nonce = secrets.token_bytes(12)
    key = derive_key(passphrase)
    chachakey = ChaCha20Poly1305(key)
    hashedkey = chachakey.encrypt(nonce, text, None)
    return nonce + hashedkey


def decrypt(blob: bytes, passphrase: str) -> bytes:
    key = derive_key(passphrase)
    nonce, ct = blob[:12], blob[12:] #splitting nonce from the key itself
    cipher = ChaCha20Poly1305(key)
    return cipher.decrypt(nonce, ct, None)