import os
import shutil
from datetime import datetime
import time

from main import args

'ffff'
# Копирует файл
if args.option == 'copy':
    flag = False
    for root, dirs, files in os.walk('main_folder'):
        if args.name in files:
            flag = True
            path = os.path.join(root, args.name)
            print(path)
            copy_path = os.path.join(root, f"{args.name}_copy")

            with open(path, 'r', encoding='utf-8') as a:
                text = a.read()
            with open(copy_path, 'w', encoding='utf-8') as b:
                b.write(text)
    if not flag:
        print('Файл не найден')


# Удаляет файл или папку
if args.option == 'delete':
    for root, dirs, files in os.walk('main_folder'):
        if args.name in files:
            flag = True
            path = os.path.join(root, args.name)
            os.remove(path)

        elif args.name in dirs:
            flag = True
            path = os.path.join(root, args.name)
            shutil.rmtree(path)

        elif args.name == 'main_folder':
            shutil.rmtree('main_folder')



# Подсчитывает количество файлов в папке (в том числе вложенные)
if args.option == 'count':
    count_dirs = 0
    count_files = 0
    path = ''
    flag = False

    for root, dirs, files in os.walk('main_folder'):
        if args.name in dirs:
            flag = True
            path = os.path.join(root, args.name)
        elif args.name == 'main_folder':
            path = 'main_folder'

    for root1, dirs1, files1 in os.walk(path):
        for d in dirs1:
            count_dirs += 1
        for f in files1:
            count_files += 1

    if not flag:
        print('Введите название папки')
    else:
        print(f'Папок: {count_dirs}, файлов: {count_files}')


if args.option == 'found':
    pass


# В названии файла добавляет дату его создания
if args.option == 'date':
    path = ''
    flag = False

    for root, dirs, files in os.walk('main_folder'):
        if args.name in dirs:
            flag = True
            path = os.path.join(root, args.name)

        elif args.name == 'main_folder':
            path = 'main_folder'

        elif args.name in files:
            path = os.path.join(root, args.name)
            ftime = os.path.getctime(path)
            new_ftime = datetime.fromtimestamp(ftime).date()
            new_path = os.path.join(root, f'{args.name}_{new_ftime}')
            os.rename(path, new_path)

        if args.recursive:
            for root1, dirs1, files1 in os.walk(path):
                for file in files1:
                    path = os.path.join(root1, file)
                    ftime = os.path.getctime(path)
                    new_ftime = datetime.fromtimestamp(ftime).date()
                    new_path = os.path.join(root1, f'{file}_{new_ftime}')
                    os.rename(path, new_path)

        elif not args.recursive:
            pass




# python functions.py date, folder3
# python functions.py date, file5.txt
# python functions.py date, main_folder

# python functions.py copy, file6.txt
# python functions.py delete, file2.txt
# python functions.py delete, folder2
# python functions.py delete, main_folder

# python functions.py count, folder1
# python functions.py count, file2.txt
# python functions.py count, main_folder


