import requests
import json
import base64
import random
import re
from transliterate import translit

# BASE_URL = 'http://127.0.0.1:8080'
# BASE_URL = 'https://blzhcoder.ctf.su'
BASE_URL = 'http://[2a03:b0c0:3:e0::3eb:1]'


def get_words(answer):
    return answer.lower().split(' ')


def get_words_by_image(path):
    r = '[{"block":"cbir-uploader__get-cbir-id"}]'
    resp = requests.post('https://yandex.ru/images/touch/search?exp_flags=images_touch_cbir&rpt=imageview&format=json', files={
        'upfile': ('', open(path, 'rb'), 'image/jpeg'),
    }, data={
        'request': r,
    })

    data = json.loads(resp.text)
    u = data['blocks'][0]['params']['url']

    resp = requests.get(f'https://yandex.ru/images/search?{u}')
    t = resp.text
    words = re.findall(r'<a class="link link_theme_normal link_ajax_yes tags__tag i-bem" data-bem=\'{"link":{}}\' target="" tabindex="\d+" href="/images/search\?text=[^"]*">([^<]*)</a>', t)
    words = [get_words(i) for i in words]
    words = [translit(word, 'ru', reversed=True) for splitted_words in words for word in splitted_words]
    words = [word for word in words if len(word) > 2]
    words = set(words)

    words.discard('png')
    words.discard('jpg')
    words.discard('gif')

    return words


template_begin = '''#!/usr/bin/env python

data = input()
D = {
'''

template_end = '''
}

suffix = data[-10:]
if D.get(suffix) is not None:
    print(D[suffix])
else:
    print(data)
'''

# STORAGE = {'nL39f/2Q==': 'slayers', 'EBAQEH/9k=': 'amelija', 'KIlESiL//Z': 'slayers', 'v4x6UdQP/Z': 'gabriev', 'y572J//9k=': 'zelgadis', 'pMTKNUQf/Z': 'glinka', 'XFMT//2Q==': 'iogann', 'Ux5r//2Q==': 'chajkovskogo', '229vjag//Z': "vasil'evich", 'csSTQB/9k=': 'modest', 'Mf+8v/2Q==': 'bekend', 'EREH//2Q==': 'perl', '2D/wCnd//Z': 'bash', 'C1RRQB/9k=': 'programmirovanija', 'AAAAD/2Q==': 'python', 'j3gn//2Q==': 'interesnye', '2KSzxn/9k=': 'matematika', 'PfPrr85//Z': 'marks', 'P+iA9bP//Z': 'moshennichestvo', 'HEGrTcf//Z': 'hristofor', 'BKjAf/2Q==': 'borody', 'U4nrPQ/9k=': 'tolstoj', 'nFRZ5PX//Z': 'portret', '2o4kf/2Q==': "n'juton", 'bAgYHNf//Z': 'kena', 'TlPE6eWP/Z': 'leonard', 'iigD//2Q==': 'lenin', 'DxNM//2Q==': 'tomas', 'hXSWz/2Q==': 'avraam', 'SlJJJJKf/Z': 'kartinki', 'XVYz//2Q==': 'anime', 'hJ/k7z/9k=': 'chelsi', 'FYyokTc//Z': 'kurome', 'FikfIxP//Z': 'ubijtsa', 'KFZGYfZ//Z': 'ubijtsa', 'Ynb/n/AP/Z': 'rwby', 'VtfRc//9k=': 'anime', 'xSmMYxSv/Z': 'dress', '8Aa+af/9k=': 'xiao', 'cUs7mP/9k=': 'kostjumy', 'jJ+J//2Q==': 'rider', 'QKGOAHP//Z': 'fate', 'P99X/9w//Z': 'zhanna', 'IaYCnSf//Z': 'fate', 'XoQmkT/9k=': 'apocrypha', 'EKNB7gf//Z': 'sao', 'M5o9fLf//Z': 'yuuki', 's2s/xlf//Z': 'anime', '75FB//2Q==': 'avu', '0s/n/3f//Z': 'sao'}
STORAGE = {}

for i in range(50):
    template = template_begin
    for suffix, answer in STORAGE.items():
        template += f'"{suffix}": "{answer}",\n'

    template += template_end

    f = open('prog.py', 'w')
    f.write(template)
    f.close()

    response = requests.post(BASE_URL + '/check', files={
        'uploadfile': open('prog.py', 'rb'),
    }).text

    print(response)

    level = re.findall(r'<b>(\d+)</b>/<b>50</b>', response)[0]
    try:
        answer = re.findall(r'тест: <b>([^<]*)</b>. <b class="text-danger">Неправильно</b>', response)[0]
    except IndexError:
        print('Invalid answer')
        # print(response)
        break

    img_data = base64.b64decode(answer)
    f = open(f'{i}.jpg', 'wb')
    f.write(img_data)
    f.close()

    words = list(get_words_by_image(f'{i}.jpg'))
    print(words)

    STORAGE.update({answer[-10:]: random.choice(words)})

    print(f'Level: {level} passed')
    print(STORAGE)
