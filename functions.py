import os
import shutil
from datetime import datetime


# Копирует файл
def copy_file(path, copy_path):
    with open(path, 'r', encoding='utf-8') as a:
        text = a.read()
    with open(copy_path, 'w', encoding='utf-8') as b:
        b.write(text)


# Удаляет файл или папку
def del_file_dir(name, name_main_dirs, path):
    for root, dirs, files in os.walk(name_main_dirs):
        if name in files:
            os.remove(path)

        elif name in dirs:
            shutil.rmtree(path)

        elif name == name_main_dirs:
            shutil.rmtree(name_main_dirs)


 # Подсчитывает количество файлов в папке (в том числе вложенные)
def count_file_dir(path):
    count_dirs = 0
    count_files = 0

    for root, dirs, files in os.walk(path):
        for _ in dirs:
            count_dirs += 1
        for _ in files:
            count_files += 1

    print(f'Папок: {count_dirs}, файлов: {count_files}')
    return count_dirs, count_files


def found_file():
    pass


# В названии файла добавляет дату его создания
def date_file(path, flag_files, flag_dirs, flag_main, rec):
    ftime = os.path.getctime(path)
    new_ftime = datetime.fromtimestamp(ftime).date()

    if flag_files:
        os.rename(path, f'{path}_{new_ftime}')

    elif (flag_dirs or flag_main) and rec:
        for root, dirs, files in os.walk(path):
            for file in files:
                os.rename(f'{root}//{file}', f'{root}//{file}_{new_ftime}')

    elif flag_dirs or flag_main:
        for root, dirs, files in os.walk(path):
            for file in files:
                os.rename(f'{root}//{file}', f'{root}//{file}_{new_ftime}')
            break

# Выводит размер файлов и папок
def analyse_dir(path):
    for root, dirs, files in os.walk(path):
        full_size = 0
        for d in dirs:
            d_path = os.path.join(root, d)
            size = 0
            for subroot, subfolder, subfiles in os.walk(d_path):
                for f in subfiles:
                    f_path = os.path.join(subroot, f)
                    size += os.path.getsize(f_path)
            full_size += size
            print(f'- Папка: {d}: {size} байт')

        for f in files:
            f_path = os.path.join(root, f)
            f_size = os.path.getsize(f_path)
            full_size += f_size
            print(f'- Файл: {f}: {f_size} байт')
        print(f'Полный размер: {full_size} байт')

        break
    return full_size