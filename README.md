# notes
### Описание:
* Сайт блогов, без регистрации пользователей.
* Просмотр всех страниц доступен только зарегистрированным в базе пользователям.
* Каждый пользователь может видеть записи других пользователей и создавать, редактировать, удалять свои записи и картинки.

Сделано покрытие тестами, тестирование запускается командой pytest из директории /notes.

### Используемые технологии:
* django==3.2.8
* requests==2.22.0
* sorl-thumbnail==12.6.3
* python-dotenv==0.19.1


### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/feyaschuk/api_yamdb.git
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt

Выполнить миграции:
```
python3 manage.py migrate
Запустить проект:
```
python3 manage.py runserver

![image](https://user-images.githubusercontent.com/81573309/137743216-8ed33bb1-e44f-4364-888f-6698ccda3583.png)

