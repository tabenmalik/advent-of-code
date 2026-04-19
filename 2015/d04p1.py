from __future__ import annotations

import hashlib
from itertools import count

import aoc


def complete_key(secret_key: str) -> int:
    # find the number (without leading zeros) such that
    # the md5 hash of f"secret_key{number}" starts with 5 zeros
    secret_key = secret_key.strip()
    for num in count(1):
        key = f"{secret_key}{num}"
        md5_hash = hashlib.md5(key.encode("ascii"), usedforsecurity=False)
        if md5_hash.hexdigest().startswith("00000"):
            break
    return num


if __name__ == "__main__":
    raise SystemExit(
        aoc.problem_entry_point(complete_key, 2015, 4),
    )


import pytest  # noqa: E402


@pytest.mark.parametrize(
    "secret_key,md5_hash",
    [
        ("abcdef", 609043),
        ("abcdef\n", 609043),
        ("pqrstuv", 1048970),
        ("pqrstuv\n", 1048970),
        (aoc.get_input(2015, 4), 254575),
    ],
)
def test_complete_key(secret_key, md5_hash):
    assert md5_hash == complete_key(secret_key)
