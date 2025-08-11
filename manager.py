import argparse
import os

from functions import copy_file, del_file_dir, count_file_dir, found_file, date_file, analyse_dir
from structure import add_structure

parser = argparse.ArgumentParser(description='Менеджер для файловой системы')

parser.add_argument('option', type=str, help='''Функции: 
                    add_structure — создать главную папку с файлами; 
                    copy — копировать файл; 
                    delete — удалить файл или папку; 
                    count — подсчитать количество файлов в папке; 
                    found — найти файлы по фильтру -f; 
                    date — добавить в название файла дату создания; 
                    analyse — показать статистику по весу файлов''')
parser.add_argument('name', help='Имя файла или папки')
parser.add_argument('--recursive', '-r', action='store_true', help='''Добавляет изменения во все файлы в папке
                                                                   на несколько уровней вложения''')
parser.add_argument('--filter', '-f', default='.', help='Фильтр для поиска файлов')

args = parser.parse_args()

path = None
copy_path = None
flag_files = False
flag_dirs = False
flag_main = False

if args.option == 'add_structure':
    add_structure(args.name)
    print(f'Главная папка {args.name} создана')
    exit()

if not os.path.isfile('main.txt'):
    print('Создайте папку с помощью add_structure')
    exit(1)

# Записываем имя главной папки
with open('main.txt', 'r', encoding='utf-8') as f:
    name_main_dir = f.read()

# Записываю путь к файлу/папке
for root, dirs, files in os.walk(name_main_dir):
    if args.name in files:
        flag_files = True
        path = os.path.join(root, args.name)
        copy_path = os.path.join(root, f'{args.name}_copy')

    elif args.name in dirs:
        flag_dirs = True
        path = os.path.join(root, args.name)

    elif args.name == name_main_dir:
        flag_main = True
        path = name_main_dir

# Если нет файла/папки - ошибка
if not flag_main and not flag_dirs and not flag_files:
    raise FileNotFoundError('Файл или папка не найдены')

options = {
    'add_structure': None,
    'copy': lambda: copy_file(path, copy_path) if flag_files else print('Введите название файла'),
    'delete': lambda: del_file_dir(args.name, name_main_dir, path),
    'count': lambda: count_file_dir(path) if flag_dirs or flag_main else print('Введите название папки'),
    'found': lambda: found_file(args.filter, path) if flag_dirs or flag_main else print('Введите название папки'),
    'date': lambda: date_file(path, flag_files, flag_dirs, flag_main, args.recursive),
    'analyse': lambda: analyse_dir(path) if flag_dirs or flag_main else print('Введите название папки')
}

print(f'Выполнена команда {args.option}, имя файла {args.name}')

if args.option in options:
    options[args.option]()
else:
    print('Неизвестная команда')

