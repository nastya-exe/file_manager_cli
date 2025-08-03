import argparse
import os

options = {
    'copy': None,
    'delete': lambda x: os.remove(x),
    'count': None,
    'found': None,
    'date': None,
    'analyse': None
}

parser = argparse.ArgumentParser(description='Менеджер для файловой системы')

parser.add_argument('option', type=str, choices=options.keys())
parser.add_argument('name', help='Имя файла или папки')
parser.add_argument('--recursive', '-r', action='store_true', help='')


args = parser.parse_args()


print(f'Выполнена команда {args.option}, имя файла {args.name}')