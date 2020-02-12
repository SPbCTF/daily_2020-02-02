import requests
import json
import re
from transliterate import translit


def get_words(answer):
    return answer.lower().split(' ')


for i in range(0, 50):
    try:
        r = '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'
        resp = requests.post(f'https://yandex.ru/images/search?rpt=imageview&format=json&request={r}', files={
            'upfile': ('', open(f'images/{i}.jpg', 'rb'), 'image/jpeg'),
        })

        data = json.loads(resp.text)
        u = data['blocks'][0]['params']['url']

        # print(data['blocks'][0]['params']['url'])

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

        print(f'{i}: {list(words)},')
    except Exception as e:
        print(e)
        break
