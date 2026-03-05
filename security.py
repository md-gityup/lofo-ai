import os
import uuid as _uuid
from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher, Type
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------------------------------- #
# Argon2id — secret hashing                                                   #
# --------------------------------------------------------------------------- #

# Parameters follow OWASP recommendations:
#   time_cost=2       — 2 iterations
#   memory_cost=65536 — 64 MB RAM per hash
#   parallelism=2     — 2 threads
_ph = PasswordHasher(
    type=Type.ID,
    time_cost=2,
    memory_cost=65536,
    parallelism=2,
    hash_len=32,
    salt_len=16,
)


def hash_secret(secret: str) -> str:
    """Return an Argon2id hash of the normalised secret."""
    return _ph.hash(_normalise(secret))


def verify_secret(secret: str, secret_hash: str) -> bool:
    """
    Constant-time comparison of *secret* against *secret_hash*.
    Returns True on match, False on any mismatch or malformed hash.
    """
    try:
        _ph.verify(secret_hash, _normalise(secret))
        return True
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def _normalise(value: str) -> str:
    """Strip whitespace and lowercase before hashing/comparing."""
    return value.strip().lower()


# --------------------------------------------------------------------------- #
# JWT handoff tokens                                                           #
# --------------------------------------------------------------------------- #

_JWT_SECRET = os.environ["JWT_SECRET"]
_ALGORITHM = "HS256"
_TOKEN_TTL_MINUTES = 15


def create_handoff_token(item_id: str) -> tuple[str, str, datetime]:
    """
    Mint a single-use HS256 JWT for the given item_id.

    Returns (token, jti, expires_at) so the caller can persist the jti
    to the used_tokens table without re-decoding.
    """
    jti = str(_uuid.uuid4())
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=_TOKEN_TTL_MINUTES)
    payload = {
        "sub": item_id,
        "jti": jti,
        "iat": now,
        "exp": expires_at,
    }
    token = jwt.encode(payload, _JWT_SECRET, algorithm=_ALGORITHM)
    return token, jti, expires_at


def decode_handoff_token(token: str) -> dict:
    """
    Validate signature and expiry; return the full payload dict.

    Raises jwt.ExpiredSignatureError or jwt.InvalidTokenError on any failure —
    callers are responsible for mapping these to HTTP responses.
    """
    return jwt.decode(token, _JWT_SECRET, algorithms=[_ALGORITHM])
