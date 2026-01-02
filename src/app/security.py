import hashlib
from passlib.hash import bcrypt

def hash_password(password: str) -> str:
    """
    Hash un mot de passe avec SHA-256 puis bcrypt.
    Supporte n'importe quelle longueur.
    """
    # 1. Convertir en bytes
    raw = password.encode("utf-8")

    # 2. Pré-hash SHA-256
    prehash = hashlib.sha256(raw).digest()

    # 3. Hasher avec bcrypt
    return bcrypt.hash(prehash)


def verify_password(password: str, hashed: str) -> bool:
    """
    Vérifie un mot de passe contre un hash bcrypt.
    """
    raw = password.encode("utf-8")
    prehash = hashlib.sha256(raw).digest()
    return bcrypt.verify(prehash, hashed)
