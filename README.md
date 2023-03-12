## Проект парсинга pep и документации Python 

### Описание
Проект представляет из себя парсер, который способен собирать информацию о документации Python и PEP.
Парсер можно запустить в нескольких режимах которые будут описаны ниже.
В функционал входит вывод информации в CLI в различных режимах и запись данных в файл.
К проекту подключено логирование. 

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке: 
```
git clone https://github.com/RabcriN/bs4_parser_pep
```
```
cd bs4_parser_pep
```
Cоздать и активировать виртуальное окружение:
Команда для установки виртуального окружения (Mac/Linux):
```
python3 -m venv env
source venv/bin/activate
```
Команда для Windows должна быть такая:
```
python -m venv venv
source venv/Scripts/activate
```
```
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Перейти в папку проекта:
```
cd src
```
# Ознакомиться с функционалом проека поможет команда
```
python main.py --help
```

# Режимы работы парсера:
```
python main.py whats-new
```
Собирает и выводит следующую информацию:
Ссылка, название и автор обновления Python
```
python main.py latest-versions
```
Собирает и выводит следующую информацию:
Ссылка, версия и статус версии Python
```
python main.py pep
```
Собирает и выводит следующую информацию:
Статус PEP, Количество PEP в данном статусе
Итоговое количество PEP