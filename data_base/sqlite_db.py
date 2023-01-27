import sqlite3 as sq

#База данных для хранения товаров
base_product = sq.connect('Cafe_Bot.db')

#База данных для хранения информации в корзине
base_cart = sq.connect('Cafe_cart.db')

#База данных для хранения информации о лайках/дизлайках
base_flag = sq.connect('Cafe_Bot_flag.db')

#Для каждой базы данных создаём переменные для работы с запросами
cur_product = base_product.cursor()
cur_cart = base_cart.cursor()
cur_flag = base_flag.cursor()

#Создание базы данных для хранения товаров
def sql_start_product():
    if base_product:
        print ('Data base connected OK!')
    base_product.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base_product.commit()

#Создание базы данных для хранения информации в корзине
def sql_start_cart():
    if base_cart:
        print ('Data base_cart connected OK!')
    base_cart.execute('CREATE TABLE IF NOT EXISTS cart(id TEXT, name TEXT, price TEXT)')
    base_cart.commit()

#Создание базы данных для хранения информации о лайках/дизлайках
def sql_start_flag():
    if base_flag:
        print ('Data base_flag connected OK!')
    base_flag.execute('CREATE TABLE IF NOT EXISTS flag(user_id TEXT, message_id TEXT)')
    base_flag.commit()

#Функция для админа для добавления товаров в меню
async def sql_add_product(state):
    async with state.proxy() as data:
        cur_product.execute('INSERT INTO menu VALUES(?, ?, ?, ?)', tuple(data.values()))
        base_product.commit()

#Функция для добавления товаров в корзину
async def sql_add_cart(state):
    async with state.proxy() as data:
        cur_cart.execute('INSERT INTO cart VALUES(?, ?, ?)', tuple(data.values()))
        base_cart.commit()

#Функция для добавления в базу информации о лайках/дизлайках
async def sql_add_flag(user_id, message_id):
    cur_flag.execute('INSERT INTO flag VALUES(?, ?)', (user_id, message_id))
    base_flag.commit()

#Открыть все позиции меню
async def sql_send_menu():
    return cur_product.execute('SELECT * FROM menu').fetchall()

#Открыть позиции из меню определенной категории
async def sql_category_menu(category):
    return cur_product.execute(f"SELECT * FROM menu WHERE name like '{category[:-1]}%'").fetchall()

#Функция для админа для удаления товара из меню
async def sql_delete_from_menu(data):
    cur_product.execute('DELETE FROM menu WHERE name == ?', (data,))
    base_product.commit()

#Функция для просмотра корзины пользователя
async def sql_read_cart(id):
    return cur_cart.execute(f"SELECT name, price FROM cart WHERE id == '{id}'").fetchall()

#Функция для очистки корзины пользователя
async def sql_clear_cart(id):
    cur_cart.execute(f"DELETE FROM cart WHERE id == '{id}'").fetchall()
    base_cart.commit()

#Функция для поиска сообщения с информацией о лайках/дизлайках пользователя
async def sql_read_flag(username, message_id):
    for i in cur_flag.execute(f"SELECT * FROM flag WHERE user_id == '{username}' and message_id == {message_id}").fetchall():
        return i

#Функция для поиска всех сообщений определенного пользователя о лайках и дизлайках
async def sql_read_flag_all(username):
    return cur_flag.execute(f"SELECT * FROM flag WHERE user_id == '{username}'").fetchall()

#Функция для очистки информации о лайках/дизлайках определенного пользователя в определенном сообщении
async def sql_clear_flag(username, message_id):
    cur_flag.execute(f"DELETE FROM flag WHERE user_id == '{username}' and message_id == {message_id}").fetchall()
    base_flag.commit()

#Функция для очистки всей информации о лайках/дизлайках определенного пользователя
async def sql_clear_username_flag(username):
    cur_flag.execute(f"DELETE FROM flag WHERE user_id == '{username}'").fetchall()
    base_flag.commit()


