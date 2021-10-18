# notes
### Описание:
* Сайт блогов, без регистрации пользователей.
* Просмотр всех страниц доступен только зарегистрированным в базе пользователям.
* Каждый пользователь может видеть записи других пользователей и создавать, редактировать, удалять свои записи и картинки.
* Сделано покрытие тестами, тестирование запускается командой pytest из директории /notes.

### Используемые технологии:
* django==3.2.8
* requests==2.22.0
* sorl-thumbnail==12.6.3
* python-dotenv==0.19.1

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone https://github.com/feyaschuk/api_yamdb.git
```
```bash
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv env
```
```bash
source env/bin/activate
```
```bash
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```
Выполнить миграции:
```bash
python3 manage.py migrate
```
Запустить проект:
```bash
python3 manage.py runserver
```
