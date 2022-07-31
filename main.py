import os
import psycopg2
import requests
import asyncio
import sheetdata
from decimal import Decimal as dec
from lxml import etree

# Данные для подключения к БД.
DATABASE=os.environ.get('POSTGRES_DB')
USER=os.environ.get('POSTGRES_USER')
PASSWORD=os.environ.get('POSTGRES_PASSWORD')
HOST='db'
PORT='5432'


class DataBaseManager():
    """Менеджер базы данных."""
    def __init__ (self):
        self.usd = self.get_usd()
        # Получаем данные с документа при помощи Google API.
        self.values = sheetdata.main()       

    
    def get_usd(self):
        """Получает данные для перевода USD в RUB."""        
        url = 'http://cbr.ru/scripts/XML_daily.asp'
        response = requests.get(url)
        response.raise_for_status()
        content = response.content
        root = etree.fromstring(content)
        id = "//Valute[@ID='R01235']/Value/text()"
        # Берем котировку USD, меняем десятичный разделитель, преобразуем в Decimal для расчетов.
        self.usd = dec(str(root.xpath(id)[0]).replace(',','.'))
        return self.usd

    
    def connect(self):
        """Подключение к базе данных."""     
        con = psycopg2.connect(database=DATABASE,user=USER,
                            password=PASSWORD, host=HOST, port=PORT)
        print ('Connected.')
        return con

    
    def populate(self):
        """Первичное заполнение БД."""
        # Запрашиваем актуальную котировку при каждом подключении к БД.
        usd = self.get_usd()  
        con = self.connect()
        cur = con.cursor()
        # Таблица пустая?
        try:
            cur.execute(f"""SELECT * FROM orders""")
        except:
            con.rollback()
            cur.execute(""" CREATE TABLE orders (
                            number integer,
                            order_no integer,
                            amount_USD numeric,
                            amount_RUB numeric,
                            delivery_date varchar
                                                );""")
            cur.execute(f"""SELECT * FROM orders""")
        rows = cur.fetchall()
        # Очищаем таблицу.
        if rows:
            cur.execute(f"""TRUNCATE orders""")
            print ('Truncating old data.')
        # Заполняем данными.
        for row in self.values:
            cur.execute(f"""INSERT INTO orders 
                        (number,order_no, amount_usd, amount_rub, delivery_date)
                        VALUES ({row[0]}, {row[1]}, {row[2]}, {dec(row[2])*usd:.2f},'{row[3]}')"""
                        )
        con.commit()
        print('The database has been populated.')
        con.close()

   
    def compare(self):
        """Сравнивает данные."""
        # Инструмент для конверсии в кортежи.
        def tuple_it(list): return[tuple(l) for l in list]
        # Сравниваем последние данные с актуальными.
        new_values = sheetdata.main()
        if self.values != new_values:
            # Готовим данные к внесению в БД.
            new_rows = set(tuple_it(new_values))-set(tuple_it(self.values))-{()} 
            deleted_rows = set(tuple_it(self.values))-set(tuple_it(new_values))
            self.values = new_values # Обновляем данные для отслеживания.
            return {'new': new_rows, 'deleted': deleted_rows} 
        return None        

    
    def update (self,updates):
        """Обновляет БД по результатам сравнения."""
        # Запрашиваем актуальную котировку при каждом подключении к БД.
        usd = self.get_usd()
        con = self.connect()
        cur = con.cursor()
        # Старые строки удаляются.
        if updates['deleted']:
            for row in list(updates['deleted']):
                cur.execute(f"""DELETE FROM orders 
                           WHERE number={row[0]}"""
                           )                
                print(f"Row deleted: {row[0]}, {row[1]}, {row[2]}, {dec(row[2])*usd:.2f},'{row[3]}")
        # Новые строки добавляются.
        if updates['new']:
            for row in list(updates['new']):
                cur.execute(f"""INSERT INTO orders 
                           (number,order_no, amount_usd, amount_rub, delivery_date)
                           VALUES ({row[0]}, {row[1]}, {row[2]}, {dec(row[2])*usd:.2f},'{row[3]}')"""
                           )
                print(f"Row added: {row[0]}, {row[1]}, {row[2]}, {dec(row[2])*usd:.2f},'{row[3]}'")
        con.commit()
        con.close()


async def main():
    REFRESH_RATE = 10 # Частота актуализации БД, сек. 
    manager = DataBaseManager()
    manager.populate()
    while True:
        await asyncio.sleep(REFRESH_RATE)
        updates = manager.compare() 
        if updates:
            manager.update(updates)


asyncio.run(main())
