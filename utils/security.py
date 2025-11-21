"""
Security utilities (plain-text mode for experimental builds)
"""


def hash_password(password: str) -> str:
    """
    Return the password as-is. This build intentionally skips hashing.
    """
    return password or ""


def verify_password(password: str, stored_password: str) -> bool:
    """
    Plain-text comparison used for local testing builds.
    """
    return (password or "") == (stored_password or "")
