from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from CreateBot import bot
from aiogram.dispatcher.filters import Text
from variables import commands
from data_base import sqlite_db
from Keyboards import del_product
from handlers.Client import send_start
from config import ID

#Создание состояний для админа для добавления/удаления позиций из меню ресторана
class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


#Реакция на /reset - сброс состояния и процесса загрузки/удаления
async def reset_state(message: types.Message, state: FSMContext):
    if await state.get_state() in commands['state_admin']:
        await state.finish()
        await message.reply('❌ Операция отменена\n❌ Состояние сброшено до начального')
    else:
        await send_start(message, state)


#Реакция на "Загрузить" - ответная просьба загрузить фото
async def admin_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMadmin.photo.set()
        await message.reply('Активирован режим загрузки товаров\nСначала <b>загрузите фотографию товара</b>', parse_mode='html')


#Записть фото в память и просьба ввести наименование товара
async def get_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMadmin.name.set()
        await message.reply('Фото корректное.\nТеперь, введите <b>наименование товара</b>', parse_mode='html')


#Запись наименования в память и просьба ввести описание товара
async def get_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMadmin.description.set()
        await message.reply('Введите <b>описание товара</b>', parse_mode='html')


#Запись описания в память и просьба ввести стоимость товара
async def get_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMadmin.price.set()
        await message.reply('Введите <b>стоимость товара</b>', parse_mode='html')


#Запись стоимость в память, запись всех данных из памяти в базу product, сброс памяти и состояния
async def get_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float (message.text)
        await message.answer('<i>Всё готово!</i>', parse_mode='html')
        await sqlite_db.sql_add_product(state)
        await state.finish()


#Реакция на команду /del, отправка всех имеющихся товаров с клавиатурой для удаления
async def menu_for_delete (message: types.Message):
    if message.from_user.id == ID:
        for i in await sqlite_db.sql_send_menu():
            await bot.send_photo(message.from_user.id, i[0], f"Наименование товара: {i[1]}\nОписание: {i[2]}\nЦена: {i[3]} руб.", reply_markup=del_product(i[1]))


#Реакция на кнопку "Удалить" - удаление товары из базы product
async def del_position(query: types.CallbackQuery):
    await sqlite_db.sql_delete_from_menu(query.data.replace('del ', ''))
    await query.answer('УДАЛЕНО')
    await query.message.delete()


#Реакция на любой стикер
async def other_stick(message: types.Message):
    await bot.send_sticker(message.from_user.id, message.sticker.file_id)
    await message.answer (f"У нас тоже есть такой стикер 😅\nВыберите доступную команду из списка ⬇\n\n"
                          f"{commands['help_info']}", parse_mode='html')


#Реакция на любое фото
async def other_photo(message: types.Message):
    await message.reply(f"Вы отправили фотографию 🤔\nПопробуйте выбрать что-то из списка ⬇\n\n{commands['help_info']}",
                        parse_mode='html')


#Реакция на любой другой текст
async def other_message(message: types.Message):
    await message.reply(f"К сожалению, такой команды нет. Попробуйте выбрать что-то из списка ⬇\n\n"
                        f"{commands['help_info']}", parse_mode='html')


#Иницилизация и запуск всех вышеперечисленных функций
def admin_handler(dp: Dispatcher):
    dp.register_message_handler(reset_state, Text(commands['reset_command'], ignore_case=True), state='*')
    dp.register_message_handler(admin_start, Text(commands['load_command'], ignore_case=True), state='*')
    dp.register_message_handler(menu_for_delete, Text(commands['del_command'], ignore_case=True), state='*')
    dp.register_message_handler(get_photo, content_types=['photo'], state=FSMadmin.photo)
    dp.register_message_handler(get_name, state=FSMadmin.name)
    dp.register_message_handler(get_description, state=FSMadmin.description)
    dp.register_message_handler(get_price, state=FSMadmin.price)
    dp.register_message_handler(other_photo, content_types=['photo'], state='*')
    dp.register_message_handler(other_stick, content_types=['sticker'], state='*')
    dp.register_message_handler(other_message, state='*')
    dp.register_callback_query_handler(del_position, lambda x: x.data and x.data.startswith('del '))



