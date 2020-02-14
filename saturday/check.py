#!/usr/bin/env python

import subprocess
import base64
from transliterate import translit, detect_language


def check(level, answer):
    global answers
    answer = answer.lower()
    if detect_language(answer) == 'ru':
        answer = translit(answer, 'ru', reversed=True)

    return answer in answers[level]


answers = {
    0: ['dazhedra', 'invers', 'inverse', 'slayers', 'lina', 'rubaki', 'slajers'],
    1: ['slajers', 'rubaki', 'yil', 'uil', 'vil', 'tesla', 'amelia', 'sejlun', 'sejrun', 'yu-gi-oh', 'slayers', 'amelija', 'art', "jubel"],
    2: ['slajers', 'slayers', 'naga', 'rubaki', 'serpent'],
    3: ['slajers', 'slayers', 'rubaki', 'gabriev', 'gabriel', 'linka', "zel'dy", 'breath', 'gauri', 'harribel'],
    4: ['rubaki', 'zelgadis', 'nekst', 'personazh', 'slayers', 'rubaki', 'grejvords', 'slajers'],

    5: ['songwriter', 'writer', 'composer', 'kompozitor', 'mikhail', 'mihail', 'ivanovich', 'glinka'],
    6: ['songwriter', 'writer', 'composer', 'kompozitor', "sebast'jan", 'nemetskaja', 'iogann', 'bah', 'marija', 'starosti', 'biografija', 'barbara', 'johann', 'sebastian', 'bach', 'hristian'],
    7: ['songwriter', 'writer', 'composer', 'kompozitor', 'chajkovskogo', 'chajkovskij', 'p.chajkovskij', 'kompozitora', 'petr', "il'ich", 'pyotr', 'ilyich', 'tchaikovsky'],
    8: ['songwriter', 'writer', 'composer', 'kompozitor', 'gorovits', 'biografija', 'rahmaninov', 'sergej', "vasil'evich", 'sergei', 'vasilyevich', 'rachmaninoff'],
    9: ['songwriter', 'writer', 'composer', 'kompozitor', 'petrovich', 'musorgskij', 'modest', 'kompozitora', 'mussorgsky'],

    10: ['programmirovanija', 'jazyk', 'bekend', 'backend', 'gopher', 'detej', 'golang', 'dlja', 'gofer', 'go', 'emblema'],
    11: ['programmirovanija', 'jazyk', 'perl', 'camel', 'logo', 'logotip', 'emblema'],
    12: ['programmirovanija', 'jazyk', 'bash', 'cube', 'logo', 'logotip', 'emblema'],
    13: ['programmirovanija', 'jazyk', 'java', 'logo', 'logotip', 'emblema'],
    14: ['programmirovanija', 'jazyk', 'python', 'logo', 'logotip', 'emblema'],

    15: ['portret', 'albert', 'einstein', "al'bert", 'pokolenie', 'mir', 'poluchit', "glupost", 'enshtejn', 'samaja', 'idiotov', 'ejnshtejn', 'interesnye', "bol'shaja", 'fakty'],
    16: ['portret', 'galileo', 'di', 'vincenzo', 'bonaulti', 'de', 'galilei', 'galileo', 'galilja', 'portret', 'teleskop', 'galilej', 'matematika'],
    17: ['portret', 'carl', 'karl', 'marx', 'marksa', 'genrih', 'levi', 'marks', 'portret', 'avu', 'karla', 'karl', 'mordehaj'],
    18: ['portret', 'elon', 'reeve', 'musk', 'mask', 'ilon', 'elon', 'moshennichestvo', 'ilona', 'kevin', 'djurand'],
    19: ['portret', 'christopher', 'columbus', 'kolumba', 'lengdell', 'columb', 'kolumb', 'fotografija', 'hristofor', 'hristofora', "otkryvatel"],
    20: ['portret', 'james', 'clerk', 'maxwell', 'dzh', 'klerk', 'bez', 'dzhejms', 'borody', 'maksvell'],
    21: ['portret', 'charles', 'robert','darwin', 'darvin', "charl'z", 'robert', 'tolstoj', 'erazm', 'darvіn'],
    22: ['portret', 'michael', 'faraday', 'majkl', 'faradej', 'uchenyj', 'portret'],
    23: ['portret', 'sir', 'isaac', 'newton', 'kachestve', 'shkoly', 'kartinki', "n'jutona", 'dlja', 'portret', 'detstve', 'horoshem', 'isaak', "n'juton"],
    24: ['portret', 'henry', 'ford', 'majlza', 'kena', 'molodosti', 'ford', 'genri', 'genrih', 'phord'],
    25: ['portret', 'leonhard', 'euler', "charl'z", 'leonard', 'ejler', 'portret'],
    26: ['portret', 'vladimir', 'ilyich', 'ulyanov', 'lenin', 'vladimir', 'lenina', 'mahatma', 'rsfsr', "il'ich", 'portret'],
    27: ['portret', 'thomas', 'alva', 'edison', "al'va", 'edіson', 'edison', 'alva', 'tomas'],
    28: ['portret', 'abraham', 'lincoln', "lincol'n", "linkoln", "linkol'n", 'vyborah', 'avraam', 'portret', 'borody', 'poster', 'bez'],
    29: ['portret', 'marco', 'polo', 'marko', 'puteshestvennik', 'kartinki', 'polo', "raspechatat'", 'dlja', 'foto', 'prezentatsii', 'fotografii'],

    30: ['akame', 'kill', 'ubijtsa', 'akame!', 'leon', 'leona', 'leone', 'ubijtsa', 'risunok', 'anime', 'art'],
    31: ['akame', 'kill', 'ubijtsa', 'akame!', 'ubijtsa', 'arty', 'chelsi', 'art', 'chelsy'],
    32: ['akame', 'kill', 'ubijtsa', 'akame!', "smert", 'kill', 'kurome', 'curome', 'akame'],
    33: ['akame', 'kill', 'ubijtsa', 'akame!', 'anime', 'akame', 'serija'],
    34: ['akame', 'kill', 'ubijtsa', 'akame!', 'main', 'majn'],

    35: ['rwby', 'vinter', 'winter', 'devushka', 'anime', 'rwby', 'shni', 'schnee', 'art'],
    36: ['rwby', 'ruby', 'rose', 'roose', 'anime', 'arty', 'rwby', 'echi'],
    37: ['rwby', 'vajs', 'weiss', 'dress', 'schnee', 'vajss', 'rwby', 'arty', 'shni'],
    38: ['rwby', 'jang', 'long', 'shao', "jan'", 'xiao', 'anime', 'arty', 'rwby', 'yellow', 'yang'],
    39: ['rwby', 'blejk', 'belladonna', 'blake', 'belladonna', 'rwby', 'kostjumy'],

    40: ["sud'ba", 'sudba', 'fate', 'stay', 'night', 'rajder', 'rider', 'fate', 'medusa'],
    41: ["sud'ba", 'sudba', 'apokrif', 'fate', 'apocrypha', 'atalanta', 'luchnitsa', 'anime', 'apocrypha', 'fate'],
    42: ["sud'ba", 'sudba', 'apokrif', 'fate', 'apocrypha', 'zhanna', 'jeane', 'jeanne', 'sudba', 'dark'],
    43: ["sud'ba", 'sudba', 'mordred', 'apokrif', "sud'ba", 'saber', 'sejber', 'apocrypha', 'fate'],
    44: ["sud'ba", 'sudba', "astol'fo", 'astolfo', 'grand', 'rajder', 'order', 'apocrypha', 'anime', 'fate', 'dakimakura'],

    45: ['mastera', 'onlajn', 'mecha', 'sao', 'sowrd', 'art', 'online', 'lizbet', 'lisbet', 'lizbett', 'lisbett', 'sinodzaki', 'rika'],
    46: ['mastera', 'onlajn', 'mecha', 'sao', 'sowrd', 'art', 'online', 'juki', 'sao', 'yuuki', 'sad', 'konno', 'art'],
    47: ['sao', 'sowrd', 'art', 'online', 'juki', 'sao', 'mastera', 'anime', 'asuna', 'onlajn', 'mecha', 'yuuki', 'asuna'],
    48: ['mastera', 'onlajn', 'mecha', 'sao', 'sowrd', 'art', 'online', 'ggo', 'avu', 'asada', 'asado', 'skrinshoty', 'sinon'],
    49: ['mastera', 'onlajn', 'mecha', 'sao', 'sowrd', 'art', 'online', 'kejko', 'sao', 'silika', 'silica', 'mastera', 'anime', 'ajano', 'mecha'],
}

for i in range(len(answers)):
    with open(f"/images/{i}.jpg", "rb") as f:
        img_data = f.read()
    img_base64 = base64.b64encode(img_data)

    try:
        decision = subprocess.run(['su', '-', 'kek', '-c', '/bin/run'], timeout=1, input=img_base64,
                                  capture_output=True)

        if decision.returncode != 0:
            print(f'INVALID {i}')
            # print(decision.stderr)
            exit(0)

        a = decision.stdout or b'<None>'
    except subprocess.TimeoutExpired:
        print(f'TIMEOUT {i}')
        exit(0)
    except Exception as e:
        print(f'INVALID {i}')
        # print(e)
        exit(0)

    a = a.decode().strip()
    if len(a) == 0:
        a = '<None>'
    result = check(i, a)
    if not result:
        print(f'NO {i} {a}')
        exit(0)

print('YES')
