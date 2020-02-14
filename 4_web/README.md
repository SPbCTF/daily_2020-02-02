# Ыжфон

[Данил Бельтюков](https://t.me/augustovich)

Давно ли вы мечтали попасть в записную книжку таких влиятельных личностей как Ыж?

Сегодня мечте суждено сбыться, просто впишите свои контакты в телефонную книжку, которую Ыж написал для себя: 
[blzhphone.ctf.su/](https://blzhphone.ctf.su/)

Возможно вам удастся пробраться в админку и достать его секретный контакт?

Исходники телефонной книжки: [blzhphone.zip](blzhphone.zip)

--------------------

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

see [sploit.py](./_dev/sploit.py)