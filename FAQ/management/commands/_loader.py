import logging
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from FAQ.management.commands.base_connect import DB_connector


# Настройки логирования
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )
# Файл с токеном
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота и диспатчера
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# Инициализация базы данных
db = DB_connector()