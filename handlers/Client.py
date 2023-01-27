from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from Keyboards import *
from CreateBot import bot
from variables import url_images, commands
from data_base.sqlite_db import *
from re import findall


# Создание состояний для клиентов
class FSMclient(StatesGroup):
    start_menu = State()


# Реакция на ввод @ThisCafeShopBot - открытие инлайн-меню
async def send_inline_kb(query: types.InlineQuery):
    await bot.answer_inline_query(inline_query_id=query.id, results=inline_kb(), cache_time=1)


# Реакция на /start - открытие начальной клавиатуры, удаление оценочных сообщений из чата и очистка базы flag
async def send_start(message: types.Message, state: FSMContext):
    await message.delete()
    await state.finish()
    await bot.send_sticker(message.from_user.id, url_images['start_sticker'])
    await message.answer(
        f'Добро пожаловать в наш ресторан-бот, {message.from_user.full_name}! 🙂\n\nВыберите <b>категорию</b> ↘️',
        reply_markup=start_commands(), parse_mode='html')
    for i in await sql_read_flag_all(message.chat.username):
        try:
            await bot.delete_message(message.chat.id, i[1])
        except:
            continue
    await sql_clear_username_flag(message.chat.username)


# Реакция на команду /help - отправляется служебная информация с доступными командами для бота
async def send_help(message: types.Message):
    await bot.send_message(message.from_user.id, text=commands['help_info'], reply_markup=keyboard_hide(),
                           parse_mode='html')
    await message.delete()


# Реакция на команду /description - отправляется информация о ресторане
async def send_description(message: types.Message):
    await bot.send_photo(message.from_user.id, url_images['description_main'], caption=commands['description_cafe'],
                         reply_markup=discription_keyboard(), parse_mode='html')
    await message.delete()


# Реакция на команду /cart - отправляется информация о состоянии корзины
async def read_cart(message: types.Message, state: FSMContext, button=False):
    await bot.delete_message(message.chat.id, message.message_id)
    if await state.get_state() is None:
        button = True
    cart = dict()
    try:
        for i, j in enumerate(await sql_read_cart(message.chat.username), 1):
            cart[f'{i}) {j[0]}'] = j[1]
        position = '\n'.join([f"{i[0]} - {i[1]} руб." for i in cart.items()])
        if not cart:
            await message.answer('🧺 Сейчас Ваша корзина пуста. Добавьте что-то из меню ⬇️',
                                 reply_markup=keyboard_hide(button))
        else:
            await message.answer(f'\n\n{position}\n\n<b>Итого</b>: {sum(map(float, cart.values()))} руб.',
                                 reply_markup=cart_keyboard(), parse_mode='html')
    except:
        await message.answer('Произошла непредвиденная ошибка')


# Реакция на /menu - открывается клавиатура с категориями меню
async def open_menu(message: types.Message):
    await message.delete()
    await FSMclient.start_menu.set()
    await message.answer('Выберите что-то из нашего <b>меню</b> ↘️', reply_markup=expand_menu(), parse_mode='html')


# Реакция на команду "Открыть меню" - открывается клавиатура с категориями меню
async def opening_menu(callback: types.CallbackQuery):
    await open_menu(callback.message)


# Реакция на команду "Бурегы", "Пиица" и т.д. - отправляются все позиции из выбранной категории
async def open_category(message: types.Message):
    await message.delete()
    try:
        for i in await sql_category_menu(message.text):
            await bot.send_photo(message.from_user.id, i[0],
                                 f"Наименование товара: <i>{i[1]}</i>\nОписание: <i>{i[2]}</i>\n\n<b>Цена:</b> {i[3]} руб.",
                                 reply_markup=cart_add_keyboard(), parse_mode='html')
    except:
        await message.answer('Произошла непредвиденная ошибка')


# Реакция на команду "Показать всё" - отправляются все позиции из всех категорий
async def open_all_menu(message: types.Message):
    await message.delete()
    try:
        for i in await sql_send_menu():
            await bot.send_photo(message.from_user.id, i[0],
                                 f"Наименование товара: <i>{i[1]}</i>\nОписание: <i>{i[2]}</i>\n\n<b>Цена:</b> {i[3]} руб.",
                                 reply_markup=cart_add_keyboard(), parse_mode='html')
    except:
        await message.answer('Произошла непредвиденная ошибка')


# Удаление текущего сообщения, реакция на команду "Скрыть"
async def close_keyboard(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        return


# Удаление текущего сообщения и очистка бащы данных с информацией о лайках и дизлайках
async def close_flag(callback: types.CallbackQuery):
    await callback.message.delete()
    try:
        await sql_clear_flag(callback.message.chat.username, callback.message.message_id)
    except:
        await callback.message.answer('Произошла непредвиденная ошибка')


# Реакция на "Показать ретсоран на карте" - отправляются координаты ресторана (карта)
async def send_location(callback: types.CallbackQuery):
    await bot.send_location(callback.from_user.id, 55.7522, 37.6156, reply_markup=keyboard_hide())


# Реакция на "Отправить контакт создателя" - отправляется контакт администратора
async def send_contact(callback: types.CallbackQuery):
    await bot.send_contact(callback.from_user.id, '79535542207', 'Bogdan', 'medvedev', reply_markup=keyboard_hide())


# Добавление информации о лайках/дизлайках в базу flag и отправка ответного соощения
async def vote_callback(callback: types.CallbackQuery):
    if not await sql_read_flag(callback.message.chat.username, callback.message.message_id):
        await sql_add_flag(callback.message.chat.username, callback.message.message_id)
        if callback.data == 'like':
            await callback.answer('Вам понравилось!')
            await callback.message.edit_text('Мы рады, что Вам понравился наш ресторан-бот ☺',
                                             reply_markup=voting_result())
        else:
            await callback.answer('Вам НЕ понравилось!')
            await callback.message.edit_text('Вам не понравился наш ресторан-бот', reply_markup=voting_result(False))
    await callback.answer('Вы уже голосовали', show_alert=True)


# Добавление в корзину выбранного товара при нажатии на "Добавить в корзину"
async def add_cart(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = callback.message.chat.username
        data['name'], = findall(r'товара: (.*)\n', callback.message.caption)
        data['price'], = findall('\d+\.\d+', callback.message.caption)
    try:
        await sql_add_cart(state)
    except:
        await callback.message.answer('Произошла непредвиденная ошибка')
    await callback.answer('ДОБАВЛЕНО!')


# Отправка сообщения, когда пользователь пытается добавить товар в корзину, находясь за пределами клавиатуры с меню
async def add_cart_exception(callback: types.CallbackQuery):
    await callback.answer('Чтобы добавить товар в корзину, сначала перейдите в меню', show_alert=True)


# Очистка корзины и соответсвующей базы, реакция на "Сброс корзины"
async def clear_cart(callback: types.CallbackQuery):
    await sql_clear_cart(callback.message.chat.username)
    await callback.answer('Корзина очищена!')
    await callback.message.delete()


# Реакция на "Оформить заказ" - изменение сообщения, очистка базы корзины и отправка оценочного сообщения
async def done_order(callback: types.CallbackQuery):
    await callback.message.edit_text(f'<b>Ваш заказ успешно оформлен</b>! ✅\n\n<u>В вашем заказе:</u>\n'
                                     f'{callback.message.text}', parse_mode='html', reply_markup=keyboard_hide())
    await callback.message.answer('Вам понравился ресторан-бот?', reply_markup=voting())
    await sql_clear_cart(callback.message.chat.username)


# Иницилизация и запуск всех вышеперечисленных функций
def client_handler(dp: Dispatcher):
    dp.register_inline_handler(send_inline_kb, state='*')
    dp.register_message_handler(send_start, Text(commands['start_command'], ignore_case=True), state='*')
    dp.register_message_handler(send_help, Text(commands['help_command'], ignore_case=True), state='*')
    dp.register_message_handler(send_description, Text(commands['description_command'], ignore_case=True), state='*')
    dp.register_message_handler(read_cart, Text(commands['cart_command'], ignore_case=True), state='*')
    dp.register_message_handler(open_menu, Text(commands['menu_command'], ignore_case=True), state='*')
    dp.register_message_handler(open_category, Text(commands['categories_menu'], ignore_case=True),
                                state=FSMclient.start_menu)
    dp.register_message_handler(open_all_menu, Text(commands['all_categories'], ignore_case=True),
                                state=FSMclient.start_menu)
    dp.register_callback_query_handler(send_location, text=['map'], state='*')
    dp.register_callback_query_handler(send_contact, text=['contact'], state='*')
    dp.register_callback_query_handler(close_keyboard, text=['close'], state='*')
    dp.register_callback_query_handler(close_flag, text=['close_flag'], state='*')
    dp.register_callback_query_handler(clear_cart, text=['reset'], state='*')
    dp.register_callback_query_handler(add_cart, text=['cart'], state=FSMclient.start_menu)
    dp.register_callback_query_handler(add_cart_exception, text=['cart'], state='*')
    dp.register_callback_query_handler(opening_menu, text=['menu'], state='*')
    dp.register_callback_query_handler(vote_callback, text=['like', 'dislike'], state='*')
    dp.register_callback_query_handler(done_order, text=['register'], state='*')
