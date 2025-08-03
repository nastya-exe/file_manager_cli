import os


os.makedirs('main_folder/folder1/folder3')
os.makedirs('main_folder/folder2')

tree = {
    'main_folder': ['file1.txt'],
    'folder1': ['file2.txt', 'file4.txt'],
    'folder2': ['file3.txt'],
    'folder1/folder3': ['file5.txt', 'file6.txt']
}

for folders, files in tree.items():
    for item in files:
        if folders != 'main_folder':
            path = f'main_folder/{folders}/{item}'
        else:
            path = f'{folders}/{item}'

        with open(path, 'w', encoding='utf-8') as file:
            file.write(f'Файл {item} в папке {folders}')