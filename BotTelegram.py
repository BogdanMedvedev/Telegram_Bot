from aiogram import executor
from CreateBot import dp
from handlers import Client, Admin
from data_base import sqlite_db

#Создание баз данных
async def on_startup(_):
    print ('Telegram bot successfully launched')
    sqlite_db.sql_start_product()
    sqlite_db.sql_start_cart()
    sqlite_db.sql_start_flag()

#Запуск обработчиков команд для бота
Client.client_handler(dp)
Admin.admin_handler(dp)

#Запуск бота и создание/включение баз данных для корзины, товаров и учёта лайков/дизлайков
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
