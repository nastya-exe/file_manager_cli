# Менеджер для файловой системы



### Структура:

- structure.py - скрипт для создания структуры папок
- manager.py - интерфейс
- functions - функции
- tests.py - тесты

### Команды:

- add_structure - добавляет папку с файлами
- copy - копирует файл
- delete - удаляет файл или папку
- count - подсчитывает количество файлов в папке (в том числе вложенные)
- found - ищет все подходящие файлы в папке (в том числе вложенные) по фильтру
- date - добавляет в название файла дату его создания
- analyse - выводит информацию сколько какой файл весит

--recursive - используется в date. Добавляет дату во все вложенные файлы в папке:  
python manager.py date folder2 -r

--filter - используется в found. Выражение по которому ищутся названия подходящих файлов  
python manager.py found main4 -f 2

Код работает только после создания файла main.txt, в котором записывается название главной папки.  
Файл main.txt создается автоматически после вызова add_structure

Если создать вторую главную папку через add_structure - файл main.txt перезапишется, тогда все действия будут
происходить
со второй папкой
***
 
python manager.py add_structure main

python manager.py copy file1.txt  
python manager.py delete folder1  
python manager.py count main  
python manager.py found main -f txt  
python manager.py date main -r  
python manager.py analyse main  


