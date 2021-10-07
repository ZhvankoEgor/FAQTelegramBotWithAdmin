import os
import sys
from FAQ.management.commands.config import db
import time

title_text = "Добрый день!\n Какой у вас вопрос?"

# Загружаем данные из базы
questions = db.get_all_questions()  # Вопросы, которые мы будем рассылать
relations = db.get_relation_question()  # Информация о связях базовых и основных вопросов

# print("refreshed")
# def checker():
#     questions2 = db.get_all_questions()
#     relations2 = db.get_relation_question()
#     if questions == questions2 and relations2 == relations:
#         print("ok")
#         time.sleep(20)
#         checker()
#     else:
#         print("Base refresh")
#         os.execv(sys.executable, [sys.executable, __file__] + sys.argv)
#         checker()
# #
# # if __name__ == '__main__':
# checker()

