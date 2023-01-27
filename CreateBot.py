from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import Token

#Переменная для хранения информации состояний
storage = MemoryStorage()

#Создание бота и передача токена
bot = Bot(Token)
dp = Dispatcher(bot, storage=storage)
