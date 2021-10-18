from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from FAQ.management.commands.keyboards.inline.callback_datas import questions, relations

# Словари для автоматического создания клавиатур и хранения ответов
dict_keyboards = {}
dict_answers = {}
for i in questions:
    dict_keyboards.update({str(i[2]): InlineKeyboardMarkup(row_width=2)})
    dict_answers.update({str(i[2]): str(i[1])})

# Клавиатура для стартовой страницы
title = InlineKeyboardMarkup(row_width=2)
for i in questions:
    if i[3]:
        button = InlineKeyboardButton(text=i[0], callback_data=f"applic,{i[2]}")
        title.insert(button)


# Функция добавления клавиатур во все вопросы
def add_button(text, callback_data):
    for key in dict_keyboards:
        try:
            if int(key):
                relations.append((text, text, callback_data, key))
        except:
            print(key + " - не число")
    dict_keyboards.update({callback_data: text})


# Добавляем клавиатуру во все вопросы
add_button("Вернуться на главную", "to_main")

# Создаём клавиатуры для дополнительных вопросов
for i in relations:
    for d in dict_keyboards.keys():
        if str(i[3]) == d:
            button = InlineKeyboardButton(text=i[0], callback_data=f"applic,{i[2]}")
            dict_keyboards[d].insert(button)
