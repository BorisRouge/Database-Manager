#!/bin/sh

sudo -u postgres psql -c "CREATE USER csuser WITH PASSWORD 'qw';"
createdb -h localhost -p 5432 -U csuser CanalServiceDB
sudo -u postgres psql -d CanalServiceDB -c 'CREATE TABLE orders (
	number integer,
	order_no integer,
	amount_USD money,
	amount_RUB money,
	delivery_date date
);'

pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt 

source venv/bin/activate
sudo gnome-terminal -- python3 djpage/manage.py runserver
sudo gnome-terminal -- python3 tgbot/bot.py
python3 main.py
