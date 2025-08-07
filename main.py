import argparse


options = {
    'add_structure': None,
    'copy': None,
    'delete': None,
    'count': None,
    'found': None,
    'date': None,
    'analyse': None
}

parser = argparse.ArgumentParser(description='Менеджер для файловой системы')

parser.add_argument('option', type=str, choices=options.keys())
parser.add_argument('name', help='Имя файла или папки')
parser.add_argument('--recursive', '-r', action='store_true', help='''Добавляет изменения во все файлы в папке
                                                                   на несколько уровней вложения''')


args = parser.parse_args()


print(f'Выполнена команда {args.option}, имя файла {args.name}')