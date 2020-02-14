# Пиратский видос

[Александр Менщиков](https://t.me/n0str)

Ыж любит прокачивать скиллы и смотреть видосы SPbCTF, но из-за коронавируса канал оказался недоступен!

Ыж нашёл пиратскую копию на приватных сценерских торрентах, но это ещё не релиз — она зашифрована новым DRM от ютуба. Помогите Ыжу посмотреть видео, пока бушует эпидемия.

DRM-модуль с ютуба: [encrypt.py](encrypt.py)

Пиратская копия видео: [торрент](flag.enc.mpeg.torrent)

--------------------

# pirate-video

Optimize bruteforce with knowledge about `hashlib.shake_256` properties. Look at prefixes.
```
>>> import hashlib
>>> hashlib.shake_256(b"flag").hexdigest(1)
'42'
>>> hashlib.shake_256(b"flag").hexdigest(2)
'42f2'
>>> hashlib.shake_256(b"flag").hexdigest(16)
'42f291e9bcfcc484be525655efc9bf18'
>>> hashlib.shake_256(b"flag").hexdigest(32)
'42f291e9bcfcc484be525655efc9bf1842e7de732c19f98605450ee5e86ca888'
>>> 
```

## encrypt
```
python3 encrypt.py
```

## decrypt
```
python3 decrypt.py
```

## Generate

Run
```
python3 main.py
```
