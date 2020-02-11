import os
from typing import Dict, Any
from binascii import unhexlify, hexlify

SALT = os.environ.get("SALT", "78787878787878")
SALT = unhexlify(SALT)

FLAG = os.environ.get("FLAG", "xxxxxxxxx")

def sign(user: Dict[str, Any]) -> str:
    to_salt = user["username"] + user["name"] + str(user["level"]) + user["phone"]
    sign = bytes([c^SALT[idx % len(SALT)] for idx, c in enumerate(to_salt.encode())])
    print(f"SALTING: {to_salt.encode()}")
    return hexlify(sign).decode()

if __name__ == "__main__":
    u = dict(username="test", name="tt", level=2000, phone="3131")
    print(sign(u))