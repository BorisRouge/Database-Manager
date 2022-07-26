Ссылка на документ Google Sheets: https://docs.google.com/spreadsheets/d/1jAO6ZKf4umY_IsRcpi3ZPrwuhxyW-zw-fz0KyLHjLS8/edit?usp=sharing

Использовалась Ubuntu 22.04 LTS
Выполнены задания 1, 2, 3, 4b(без React), 4c.


ИНСТРУКЦИЯ:

Предполагается наличие установленных python и postgresql.

Запустить в корневой папке через bash-терминал скрипт start-app.sh,
который от имени пользователя postgres создает базу данных CanalServiceDB
и таблицу в ней, устанавливает виртуальное окружение, запускает его, 
устанавливает необходимые зависимости из requirements.txt, запускает
основной скрипт БД-менеджера main.py, скрипт телеграм-бота bot.py,
django-сервер.

!____________________________
В:

main.py
tgbot/bot.py
djpage/overview/views.py

в начало вынесены глобальные переменные с данными для подключения к postgresql,
укажите необходимое, например, пароль.
____________________________
