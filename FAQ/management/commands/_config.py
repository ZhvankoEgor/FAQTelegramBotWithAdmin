import os
from dotenv import load_dotenv
from FAQ.management.commands._sqliter import dbconnector

# Указываем файл с токеном и базу данных
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
db = dbconnector("/media/sf_Projects/AdminForFAQ/db.sqlite3")
