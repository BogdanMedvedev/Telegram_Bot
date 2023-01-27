#Информация /help со списком команд
help_info ='''<b>/help</b>  →  Список команд
<b>/start</b>  →  Вернуться в начало
<b>/description</b>  →  Информация о ресторане
<b>/menu</b>  →  Посмотреть меню/Оформить заказ
<b>/cart</b>  →  Посмотреть корзину

Вместо команд /cart, /menu, /description, /start, вы можете использовать команды "корзина", "меню", "описание", "старт". Символ "/" можно не использовать и регистр не важен. Также вы можете ввести в начале сообщения @ThisCafeShopBot, и бот предложит вам варианты команд.'''

#Описание ресторана для /description
description_cafe = 'Ресторан <b><i>Cafe shop 🍷</i></b>\n\n<i>В нашем ресторане вы найдёте блюда на любой вкус!</i>\n\n' \
                   '<u>Режим работы:</u>\nПонедельник — Пятница: <b>10:00 - 21:00</b>\n' \
                   'Суббота — Воскресенье: <b>9:00 - 23:00</b>\n\n<u>Телефоны:</u>\n+7 (499) 999-99-99\n' \
                   '+7 (999) 999-99-99\n\n<u>Адрес:</u>\nг. Москва, ул. Бургерная, д.7'

#Команды для старта
start_command = ['/start', '/launch', '/begin', '/forward', '/run', '/hi', 'start', 'launch', 'begin', 'forward', 'run',
                 'hi', 'restart', '/старт', 'старт', 'пуск', 'начать', 'привет', 'hello', '/go', 'go', 'вперед',
                 'вперёд', 'запуск', 'запуск бота', 'перезапуск бота', 'рестарт', 'перезапуск', 'вернуться в начало',
                 'начало', 'в начало', 'вернуться назад', 'сброс', '/cnfhn', 'cnfhn']

#Команды для открытия меню
menu_command = ['/menu', 'menu', '/меню', 'меню', 'меню ресторана', 'меню кафе', 'открыть меню']

#Команды для вызова списка доступных команд
help_command = ['/help', '/hepl', '/hlep', '/hpel', 'help', 'hepl', 'hlep', 'hpel','/command', '/commands', 'command',
               'commands', '/команды', 'команды','доступные команды','/помощь', 'помощь', '/хелп', 'хелп', 'ъэлп',
               'хэлп', 'что умеет бот', 'что умеет бот?']

#Команды для отображения описания
description_command = ['/description', 'description', '/info', 'info', '/information', 'information', '/описание',
                       'описание', '/информация', 'информация', 'о ресторане', 'о кафе']

#Команды для просмотра/вызова корзины
cart_command = ['/cart', 'cart', '/card', 'card','/корзина', '/корзина', '/коризна', '/крозина', 'корзина', 'коризна',
                'крозина', 'открыть корзину',
               'посмотреть корзину', 'просмотреть корзину']

#Команды для админа вызова меню загрузки новых товаров
load_command = ['/load', 'load','/загрузить', 'загрузить', 'загрузка', '/загрузка','/добавить', 'добавить',
                'добавить товар', '/новый','новый','новый товар']

#Команды для админа вызова меню удаления товаров
del_command = ['/remove','/del','/delete','remove','del','delete', '/удалить', 'удалить', '/удаление', 'удаление']

#Команды для админа для сброса состояния
reset_command = ['/reset', 'reset', '/cancel', '/отмена', 'cancel', 'отмена']

#Все состояния в меню администратора
state_admin = ['FSMadmin:photo', 'FSMadmin:name', 'FSMadmin:description', 'FSMadmin:price']

#Команды для просмотра определенной категории меню
categories_menu = ['Бургеры', 'Пицца', 'Десерт', 'Каша']

#Команды для просмотра всех категорий меню
all_categories = ['Показать всё']

#Приветсвенный стикер
sticker = 'CAACAgIAAxkBAAEHN6Fjv_3QrK_Ja8BQbUdjwgmoYzU2ZwACVQIAAladvQqsSyyCT6MV3y0E'

#Картинка ресторана для /description
description_main = 'https://ie.wampi.ru/2023/01/23/DDDD-1.jpg'

#Картинка ресторана для инлайн-режима @ThisCafeShopBot
description_inline = 'https://static.tildacdn.com/tild3939-3238-4365-b963-663332363831/5iFW9iLFHM8.jpg'

#Картинка меню для инлайн-режима @ThisCafeShopBot
menu_inline = 'https://ie.wampi.ru/2023/01/23/Menu.png'

#Картинка корзины для инлайн-режима @ThisCafeShopBot
cart_inline = 'https://kartinkin.net/uploads/posts/2021-07/1627081824_19-kartinkin-com-p-korzina-produktov-yeda-krasivo-foto-23.jpg'

#Картинка доступных команд для инлайн-режима @ThisCafeShopBot
help_inline = 'https://im.wampi.ru/2023/01/25/image37ef0e6745b888d2.png'

#Словари для удобного использования url и команд в хэндлерах и клавиатурах
url_images, commands = dict(), dict()

#Наполнение словарей данными
url_images['start_sticker'], url_images['help_inline'] = sticker, help_inline
url_images['description_main'], url_images['description_inline'] = description_main, description_inline
url_images['menu_inline'], url_images['cart_inline'] = menu_inline, cart_inline
commands['start_command'], commands['menu_command'] = start_command, menu_command
commands['help_info'], commands['help_command'] = help_info, help_command
commands['description_command'], commands['description_cafe'] = description_command, description_cafe
commands['load_command'], commands['del_command'] = load_command, del_command
commands['cart_command'], commands['categories_menu'] = cart_command, categories_menu
commands['all_categories'], commands['reset_command'] = all_categories, reset_command
commands['state_admin'] = state_admin
