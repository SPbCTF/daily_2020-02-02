# blzhphone

## Build

`docker-compose up` -> port 80

OR

_backend -> port 8000:_
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app
```

_frontend_ -> port 3000:
```bash
cd frontend
yarn
yarn start
```

## Exploit

see [sploit.py](./sploit.py)