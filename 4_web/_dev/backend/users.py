from io import StringIO
from typing import Dict, Any, Union, Optional
from yamldb import Db
import yaml
from passlib.context import CryptContext
from pydantic import BaseModel
import sss

class User(BaseModel):
    username: str
    level: int = 0
    phone: Optional[str] = ""
    name: Optional[str] = ""

class UserWithPassword(User):
    password: str

class EditableUser(BaseModel):
    name: Optional[str]
    phone: Optional[str]

class Users:
    _TEMPLATE = """{username}:
  password: {password}
  level: {level}
  phone: \"{phone}\"
  signature: {signature}
  name: \"{name}\"
"""

    def __init__(self, db: Db, hasher: CryptContext):
        self.db = db
        self.hasher = hasher

    def get(self, username: str) -> User:
        if username in self.db.data:
            user_data = self.db.data[username]
            user_data.pop("username", None)
            return UserWithPassword(username=username, **user_data)

    def insert_or_update(self, user: Union[User, UserWithPassword], hash_password: bool = True):
        if not user.username:
            raise "Username not specified"
        
        data_backup = self.db.data.copy()
        user_data = dict(user)
        
        if 'password' in user.fields and user.password and hash_password:
            user_data["password"] = self.get_password_hash(user.password)


        if user.username in self.db.data:
            existsing_user = self.db.data[user.username]
            existsing_user.update(user_data)
            user_data = existsing_user
        else:
            user_data["signature"] = sss.sign(user_data)
            print(f"UPDATED SIGNATURE FOR USER: {user_data}")
            
        self.db.data[user.username] = user_data

        try:
            self._write()
        except Exception as e:
            self.db.data = data_backup
            raise e

        return self.get(user.username)
        
    def _write(self):
        raw = ""
        for username, user in self.db.data.items():
            u = user
            u["username"] = username
            u.update(dict(UserWithPassword(**user)))
            if not 'signature' in u:
                u["signature"] = ""
            test_valid = self._TEMPLATE.format(**u)
            try:
                yaml.safe_load(StringIO(test_valid))
            except Exception:
                print(f"SKIP: {u}")
                continue
            raw += test_valid
        self.db.write(raw)
        self.db.read()

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.hasher.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.hasher.hash(password)

    def authenticate(self, username: str, password: str) -> Union[bool, UserWithPassword]:
        user = self.get(username)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

    

    