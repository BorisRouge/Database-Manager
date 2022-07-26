from django.shortcuts import render
from django.http import HttpResponse
from .models import Orders
import psycopg2

# Данные для подключения к БД.
DATABASE='CanalServiceDB'
USER='postgres'
PASSWORD='postgres'
HOST='127.0.0.1'
PORT='5432'


def index(request):
    con = psycopg2.connect(database=DATABASE,user=USER,
                            password=PASSWORD, host=HOST, port=PORT)   
    cur = con.cursor()
    cur.execute(f"""SELECT * FROM orders""")
    results = cur.fetchall()    
    return render(request, 'overview.html', {'context':results})