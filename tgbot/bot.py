import os
import psycopg2
import time
from datetime import date, datetime
from telegram.ext import Updater, CommandHandler

# Данные для подключения к БД.
DATABASE=os.environ.get('POSTGRES_DB')
USER=os.environ.get('POSTGRES_USER')
PASSWORD=os.environ.get('POSTGRES_PASSWORD')
HOST='db'
PORT='5432'

API_KEY = '5540061460:AAGYbJcQFKJD0stTyV_avdY_8qDuIrpKNWw'


def start (update, context):
    """Отслеживает сроки поставки."""
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id,
                                text=f'Ведется мониторинг сроков поставки.')
    # Подключаемся и запрашиваем данные с БД.
    while True:
        con = psycopg2.connect(database=DATABASE,user=USER,
                            password=PASSWORD, host=HOST, port=PORT)    
        cur = con.cursor()
        cur.execute(
            """SELECT order_no, delivery_date FROM orders
            ORDER BY reverse(delivery_date)""")
        results = cur.fetchall()        
        # Проверяем сроки поставки.
        overdue = []
        today = date.today()
        for result in results:
            date_iso = datetime.strptime(result[1],'%d.%M.%Y').date()
            if date_iso <= today:
                overdue.append(result)
        # Сообщаем результат.
        if overdue:        
            # Отбираем 10 заказов, чтобы не перегружать сообщение.                        
            ten_orders =[] 
            for order in overdue[0:10]:        
                ten_orders.append(order[0])            
            text_message = f"""
            Даты просрочены у заказов {str(ten_orders)[1:-1]} и {len(overdue)-10} других.
            """
            context.bot.send_message(chat_id,
                                text=text_message,)
            context.bot.send_message(chat_id,
                                text='Следующая проверка через 24 часа.',)
        time.sleep(86400)


def main():   
  updater = Updater(API_KEY)
  dp = updater.dispatcher
  dp.add_handler(CommandHandler('start',start))
  updater.start_polling()
  updater.idle()


if __name__ == '__main__':
  main()