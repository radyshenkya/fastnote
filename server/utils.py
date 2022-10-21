from random import choices
from hashlib import md5


NOTE_ID_LENGTH = 8
USER_TOKEN_ITERATIONS = 32
GENERATION_ALPHABET = "abcdefghijklmnopqrst1234567890"

HASH_SALT = "test_hash_salt"


def generate_new_note_id() -> str:
    from random import choices

    return "".join(choices(GENERATION_ALPHABET, k=NOTE_ID_LENGTH))


def generate_user_token() -> str:
    return md5(
        ("".join(choices(GENERATION_ALPHABET, k=USER_TOKEN_ITERATIONS))).encode("utf-8")
    ).hexdigest()


def hash_str(original_string: str) -> str:
    return md5(
        md5((HASH_SALT + original_string).encode("utf-8")).hexdigest().encode("utf-8")
    ).hexdigest()
