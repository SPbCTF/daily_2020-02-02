# Нанотехнологии

## Описание
[Артур Ханов](https://t.me/awengar)

Кто-то хранит свои пароли в текстовом файлике. 
Ыж хранит свой пароль в текстовом *редакторе*.

Вы заметили издалека, что Ыж нажимает какую-то комбинацию клавиш, когда ему нужно залогиниться.

Редактор с компьютера Ыжа: [nano](nano)

## Решение
На каждой 37-й секунде системного времени по нажатию на CTRL_E выводится флаг, он расшифровывается ксором. Во вложении diff-файл с патчем, внесенным в исходные коды nano (https://github.com/madnight/nano), скомпилированный файл с редактором. 

Узнать об этом можно было
 - из списка функций в IDA Pro, так как символы не удалялись
 - из списка перехватчиков клавишь в global.c путем сравнения списка вызовов функции add_to_sclist
 - путем сравнения бинарных файлов оригинального и модифицированного nano

Флаг FLAG:Yzh_15_H1DD3N_H3R3
