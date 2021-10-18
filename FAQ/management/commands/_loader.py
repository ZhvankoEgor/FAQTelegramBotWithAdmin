import logging
import FAQ.management.commands._config as config
from aiogram import Bot, Dispatcher

# Настройки логирования
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )

# Инициализация бота и диспатчера
bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)