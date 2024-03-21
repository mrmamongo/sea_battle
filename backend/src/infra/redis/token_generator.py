import hashlib
import uuid


def generate_token(username: str) -> str:
    return hashlib.sha256(f"{str(uuid.uuid4())}-{username}".encode()).hexdigest()
