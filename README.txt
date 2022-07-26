Ссылка на документ Google Sheets: https://docs.google.com/spreadsheets/d/1jAO6ZKf4umY_IsRcpi3ZPrwuhxyW-zw-fz0KyLHjLS8/edit?usp=sharing

Использовалась Ubuntu 22.04 LTS
Выполнены задания 1, 2, 3, 4b(без React), 4c.


ИНСТРУКЦИЯ:

Предполагается наличие установленных python и postgresql.

Запустить в корневой папке через bash-терминал скрипт start-app.sh,
который создает базу данных CanalServiceDB 
(спрашивает сначала пароль для sudo, затем введите пароль "qw" )
и таблицу в ней, устанавливает виртуальное окружение, запускает его, 
устанавливает необходимые зависимости из requirements.txt, запускает
основной скрипт БД-менеджера main.py, скрипт телеграм-бота bot.py,
django-сервер.

В любом случае, для работы приложения должны быть запущены "djpage/manage.py runserver" "tgbot/bot.py" и "python3 main.py".

Уведомления в телеграм приходят от бота https://t.me/CanalServiceTest_bot. Мониторинг запускается командой /start, интервал уведомлений 1 сутки.

!____________________________
В:

main.py
tgbot/bot.py
djpage/overview/views.py

в начало вынесены глобальные переменные с данными для подключения к postgresql,
при необходимости измените их.
____________________________
