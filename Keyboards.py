from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,\
    InlineKeyboardMarkup, InlineKeyboardButton, InputTextMessageContent, InlineQueryResultArticle
from variables import url_images

#Клавиатура в инлайн-режиме для общения с ботом через @ThisCafeShopBot
def inline_kb():
    item = InlineQueryResultArticle(input_message_content=InputTextMessageContent('/menu'), id='1',
                                    title = 'Меню ресторана', thumb_url=url_images['menu_inline'])
    item2 = InlineQueryResultArticle(input_message_content=InputTextMessageContent('/cart'), id='2',
                                     title='Посмотреть корзину', thumb_url=url_images['cart_inline'])
    item3 = InlineQueryResultArticle(input_message_content=InputTextMessageContent('/description'), id='3',
                                     title='Описание ресторана', thumb_url=url_images['description_inline'])
    item4 = InlineQueryResultArticle(input_message_content=InputTextMessageContent('/help'), id='4',
                                     title='Доступные команды', thumb_url=url_images['help_inline'])
    return [item, item2, item3, item4]

#Стартовая клавиатура
def start_commands():
    start_cm = ReplyKeyboardMarkup(resize_keyboard=True)
    start_cm.add(KeyboardButton('О ресторане'), KeyboardButton('Меню ресторана'), KeyboardButton('Корзина'),
                 KeyboardButton('Что умеет бот?'))
    return start_cm

#Клавиатура для просмотра категорий меню
def expand_menu():
    exp_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    exp_menu.add(KeyboardButton('Пицца'), KeyboardButton('Бургеры'), KeyboardButton('Каша'),
                 KeyboardButton('Десерт'), KeyboardButton('Показать всё'), KeyboardButton('Открыть корзину'),
                 KeyboardButton('Вернуться в начало'))
    return exp_menu

#Клавиатура для корзины
def cart_keyboard():
    cart_kb = InlineKeyboardMarkup(row_width=2)
    cart_kb.add(InlineKeyboardButton('Оформить заказ', callback_data='register'),
                InlineKeyboardButton('Сбросить корзину', callback_data='reset'))
    return cart_kb

#Клавиатура для добавления товара в корзину
def cart_add_keyboard():
    cart_add_kb = InlineKeyboardMarkup(row_width=2)
    cart_add_kb.add(InlineKeyboardButton('Добавить в корзину', callback_data='cart'),InlineKeyboardButton('Скрыть позицию', callback_data='close'))
    return cart_add_kb

#Клавиатура для описания ресторана
def discription_keyboard():
    discription_kb = InlineKeyboardMarkup(row_width=1)
    discription_kb.add (InlineKeyboardButton('Показать ресторан на карте', callback_data='map'),
                        InlineKeyboardButton('Показать контакт создателя', callback_data='contact'),
                        InlineKeyboardButton('Скрыть сообщение', callback_data='close'))
    return discription_kb

#Клавиатура для скрытия сообщения и открытия категорий меню
def keyboard_hide(menu=False):
    keyboard_empty_cart = InlineKeyboardMarkup(row_width=1)
    if menu:
        keyboard_empty_cart.add(InlineKeyboardButton('Открыть меню', callback_data='menu'))
        keyboard_empty_cart.add(InlineKeyboardButton('Скрыть сообщение', callback_data='close'))
        return keyboard_empty_cart
    keyboard_empty_cart.add(InlineKeyboardButton('Скрыть сообщение', callback_data='close'))
    return keyboard_empty_cart

#Клавиатура администратора для удаления товаров из меню
def del_product(callback_data):
    del_kb = InlineKeyboardMarkup(row_width=1)
    del_kb.add(InlineKeyboardButton('Удалить товар из меню', callback_data=f'del {callback_data}'))
    return del_kb

#Клавиатура для голосования
def voting():
    voting_kb = InlineKeyboardMarkup(row_width=2)
    voting_kb.add(InlineKeyboardButton('Мне нравится 👍', callback_data='like'),
                  InlineKeyboardButton('Мне не нравится 👎', callback_data='dislike'),
                  InlineKeyboardButton('Закрыть', callback_data='close_flag'))
    return voting_kb

#Клавиатура после голосования, если пользователь выбрал "Мне нравится"
def voting_result(like=True):
    like_voted = InlineKeyboardMarkup(row_width=2)
    close_button = InlineKeyboardButton('Закрыть', callback_data='close_flag')
    if like:
        like_voted.add(InlineKeyboardButton('Вам понравилось ☺', callback_data='like'), close_button)
        return like_voted
    like_voted.add(InlineKeyboardButton('Вам не понравилось ☹', callback_data='dislike'), close_button)
    return like_voted

