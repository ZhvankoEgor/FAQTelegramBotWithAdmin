import logging
import os
import sys
# from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from FAQ.management.commands.base_connect import BotQueries


# Настройки логирования

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )

BOT_TOKEN = sys.argv[2]


# Инициализация базы данных
db = BotQueries(BOT_TOKEN)

# Инициализация бота и диспатчера
try:
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(bot)
    print(f"Включен бот ID = {db.bot_id}")
    db.change_bot_status(status='включен',token=str(BOT_TOKEN))
except BaseException as err:
    print(f"Ошибка в значении токена ID = {db.bot_id}")
    db.change_bot_status(status='неверный токен',token=str(BOT_TOKEN))