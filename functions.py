import os
import shutil
from datetime import datetime
import structure
from main import args
from structure import add_structure

path = ''
copy_path = ''
flag_files = False
flag_dirs = False
flag_main = False
main_folder = None


# Записываю путь к файлу/папке
for root, dirs, files in os.walk('main_folder'):
    if args.name in files:
        flag_files = True
        path = os.path.join(root, args.name)
        copy_path = os.path.join(root, f"{args.name}_copy")

    elif args.name in dirs:
        flag_dirs = True
        path = os.path.join(root, args.name)

    elif args.name == 'main_folder':
        flag_main = True
        path = 'main_folder'


# Если нет файла/папки - ошибка
if not flag_main and not flag_dirs and not flag_files:
    raise FileNotFoundError('Файл или папка не найдены')


# Копирует файл
if args.option == 'copy':
    if flag_files:
        with open(path, 'r', encoding='utf-8') as a:
            text = a.read()
        with open(copy_path, 'w', encoding='utf-8') as b:
            b.write(text)
    else:
        print('Введите название файла')


# Удаляет файл или папку
if args.option == 'delete':
    for root, dirs, files in os.walk('main_folder'):
        if args.name in files:
            os.remove(path)

        elif args.name in dirs:
            shutil.rmtree(path)

        elif args.name == 'main_folder':
            shutil.rmtree('main_folder')


# Подсчитывает количество файлов в папке (в том числе вложенные)
if args.option == 'count':
    if flag_dirs or flag_main:
        count_dirs = 0
        count_files = 0

        for root, dirs, files in os.walk(path):
            for d in dirs:
                count_dirs += 1
            for f in files:
                count_files += 1

        print(f'Папок: {count_dirs}, файлов: {count_files}')
    else:
        print('Введите название папки')


if args.option == 'found':
    pass


# В названии файла добавляет дату его создания
if args.option == 'date':
    ftime = os.path.getctime(path)
    new_ftime = datetime.fromtimestamp(ftime).date()

    if flag_files:
        os.rename(path, f'{path}_{new_ftime}')

    elif (flag_dirs or flag_main) and args.recursive:
        for root, dirs, files in os.walk(path):
            for file in files:
                os.rename(f'{root}//{file}', f'{root}//{file}_{new_ftime}')

    elif flag_dirs or flag_main:
        for root, dirs, files in os.walk(path):
            for file in files:
                os.rename(f'{root}//{file}', f'{root}//{file}_{new_ftime}')
            break

if args.option =='analyse':
    total_size = 0
    size = 0
    for root, dirs,files in os.walk(path):

    #     for dir in dirs:
    #         print(f'Папка: {dir} {os.path.getsize(f'{root}//{dir}')}')

        for file in files:
            print(f'Файл: {file} {os.path.getsize(f'{root}//{file}')}')
        break

# python functions.py analyse, folder1
# python functions.py analyse, main_folder
# python functions.py analyse, file4.txt

# python functions.py date, folder1
# python functions.py date, main_folder
# python functions.py date, file4.txt


# python functions.py copy, file4.txt
# python functions.py copy, folder2

# python functions.py delete, file2.txt
# python functions.py delete, folder2
# python functions.py delete, main_folder

# python functions.py count, folder1
# python functions.py count, file2.txt
# python functions.py count, main_folder

# python functions.py add_structure main
