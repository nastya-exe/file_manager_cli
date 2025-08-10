import unittest
import tempfile
import os
import shutil
import subprocess
import sys

from datetime import date
from functions import copy_file, del_file_dir, count_file_dir, date_file, analyse_dir
from structure import add_structure


class TestFunctions(unittest.TestCase):
    def setUp(self):
        # в папке test_dir создаю папку dir_in_dir, в ней создаю dir_in_dir_in_dir
        self.test_dir = tempfile.mkdtemp()
        self.dir_in_dir = os.path.join(self.test_dir, 'd1')
        os.makedirs(self.dir_in_dir)

        self.dir_in_dir_in_dir = os.path.join(self.dir_in_dir, 'd2')
        os.makedirs(self.dir_in_dir_in_dir)

        #Создаю файлы file_test, file1, file2 в каждой из папок соответственно
        self.path = os.path.join(self.test_dir, 'file_test.txt')
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write('123456fghj')
        self.copy_path = os.path.join(self.test_dir, 'copy.txt')

        self.path_file1 = os.path.join(self.dir_in_dir, 'file1.txt')
        self.path_file2 = os.path.join(self.dir_in_dir_in_dir, 'file2.txt')
        with open(self.path_file1, 'w') as f:
            f.write('1234')
        with open(self.path_file2, 'w') as f:
            f.write('56789')

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        # if os.path.exists('test_dir'):
        #     shutil.rmtree('test_dir')
        # if os.path.exists('main.txt'):
        #     os.remove('main.txt')

    def test_copy_file(self):
        copy_file(self.path, self.copy_path)
        self.assertTrue(os.path.isfile(self.copy_path))
        with open(self.copy_path, 'r', encoding='utf-8') as f:
            text = f.read()
        self.assertEqual(text, '123456fghj')

    #Удаляет ли delete файл
    def test_del_file(self):
        del_file_dir('file_test.txt', self.test_dir, self.path)
        self.assertFalse(os.path.exists(self.path))

    #Удаляет ли delete папку
    def test_del_dir(self):
        del_file_dir('d1', self.test_dir, self.dir_in_dir)
        self.assertFalse(os.path.exists(self.dir_in_dir))

    def test_count_file_dir(self):
        dirs, files = count_file_dir(self.test_dir)
        self.assertEqual(dirs, 2)
        self.assertEqual(files, 3)

    #Добавляет ли дату date в имя файла
    def test_date_file_in_file(self):
        current_date = date.today().isoformat()
        new_path = f'{self.path_file1}_{current_date}'
        date_file(self.path_file1, True, False, False, False)
        self.assertTrue(os.path.exists(new_path))

    #Добавляет ли дату date в имя файлов в папке
    def test_date_file_in_dir(self):
        current_date = date.today().isoformat()
        new_path1 = f'{self.path_file1}_{current_date}'
        date_file(self.dir_in_dir, False, True, False, False)
        self.assertTrue(os.path.exists(new_path1))

    #Добавляет ли дату date в имя файлов в папке и в под-папках
    def test_date_file_in_dir_rec(self):
        current_date = date.today().isoformat()
        new_path1 = f'{self.path_file1}_{current_date}'
        new_path2 = f'{self.path_file2}_{current_date}'
        date_file(self.dir_in_dir, False, True, False, True)
        self.assertTrue(os.path.exists(new_path1))
        self.assertTrue(os.path.exists(new_path2))

    def test_analyse_dir(self):
        with open(self.path_file1, 'r') as f:
            text1 = f.read()
        with open(self.path_file2, 'r') as f:
            text2 = f.read()
        size = len(text2) + len(text1)
        self.assertEqual(size, analyse_dir(self.dir_in_dir))


class TestCli(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()





