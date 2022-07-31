import os
from django.shortcuts import render
import psycopg2

# Данные для подключения к БД.
DATABASE=os.environ.get('POSTGRES_DB')
USER=os.environ.get('POSTGRES_USER')
PASSWORD=os.environ.get('POSTGRES_PASSWORD')
HOST='db'
PORT='5432'


def index(request):
    con = psycopg2.connect(database=DATABASE,user=USER,
                            password=PASSWORD, host=HOST, port=PORT)   
    cur = con.cursor()
    cur.execute(f"""SELECT * FROM orders""")
    results = cur.fetchall() 

    return render(request, 'overview.html', {'context':results})