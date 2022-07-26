#!/bin/sh

createdb -h localhost -p 5432 -U postgres CanalServiceDB
sudo -u postgres psql -d TestDBB -c 'CREATE TABLE orders (
	number integer,
	order_no integer,
	amount_USD money,
	amount_RUB money,
	delivery_date date
);'

pip install virtualenv
virtualenv venv
source venv/bin/activate
pip intall -r requirements.txt 

python3 main.py
python3 tgbot/bot.py
python3 djpage/manage.py runserver