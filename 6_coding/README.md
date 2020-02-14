# Кто на картинке?

[Роман Опякин](https://t.me/sinketsu)

Ыж, так же как и вы, любит прокачивать знания. Сегодня он пытается решить олимпиадную задачку на программирование!

Он уже почти прошел, сможете ли вы его обогнать?

[blzhcoder.ctf.su/](https://blzhcoder.ctf.su/)

--------------------

## blzhcoder

Category: `PPC`

Requirements: `Go (v1.13+), docker`

### Build
```shell script
go build .
chmod -R 700 images
chmod +x check.py
```

### Run
```shell script
LISTEN=:80 OPS_LISTEN=127.0.0.1:81 FLAG=<flag> ./ppc
```

### Configure
All configuration via ENV

`LISTEN` - address to bind web server

`OPS_LISTEN` - address to bind to server metrics (Prometheus format)

`FLAG` - flag

### Thanks
I thank [@rive_n](https://t.me/rive_n) for the message about bug with `/images` permissions on this task.

### Sploit
See [solver.py](_dev/solver.py)
