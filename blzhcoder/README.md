## blzcoder

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
I thank [@rive_n](tg://resolve?domain=rive_n) for the message about bug with `/images` rights on this task.

### Sploit
See [solver.py](https://github.com/SPbCTF/daily_2020-02-02/blob/master/blzhcoder/check.py)