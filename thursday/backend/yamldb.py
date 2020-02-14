from typing import Optional, Dict, Any, Union
import os
from threading import Lock
import yaml


class Storage:
    def __init__(self, filepath: str):
        self.lock = Lock()
        
        self.filepath = os.path.expanduser(filepath)
        

        # Create file if necessary
        self._touch(self.filepath, True)
        self._handle = open(filepath, 'r+')

    def _touch(self, fname: str, create_dirs: bool) -> None:
        if create_dirs:
            base_dir = os.path.dirname(fname)
            print(base_dir)
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)

        if not os.path.exists(fname):
            with open(fname, 'a'):
                os.utime(fname, None)

    def read(self) -> bytes:
        with self.lock:
            # Get the file size
            self._handle.seek(0, os.SEEK_END)
            size = self._handle.tell()

            if not size:
                # File is empty
                return None
            else:
                self._handle.seek(0)
                return self._handle.read()
    
    def write(self, data: Union[str, bytes]) -> None:
        if isinstance(data, bytes):
            data = data.decode() 
        with self.lock:
            self._handle.seek(0)
            self._handle.write(data)
            self._handle.flush()
            os.fsync(self._handle.fileno())
            self._handle.truncate()

    def close(self) -> None:
        self._handle.close()
        self._handle = None

    @property
    def opened(self) -> bool:
        return not (self._handle is None)


class Db:
    def __init__(self, filepath: str):
        self.storage = Storage(filepath)
        self._raw = self.storage.read()
        if self._raw:
            self.data = self.validate(self._raw)
        else:
            self.data = dict()

    def validate(self, data: Union[str, bytes]) -> Dict[str, Dict[str, Any]]:
        parsed = yaml.safe_load(data)
        return parsed

    def write(self, data):
        try:
            self.validate(data)
        except yaml.error.YAMLError as e:
            raise ValueError("Error validating data", e)

        self.storage.write(data)
        self._raw = data
        self.data = self.validate(self._raw)
    
    def read(self):
        self._raw = self.storage.read()        
        self.data = self.validate(self._raw)
        return self.data
