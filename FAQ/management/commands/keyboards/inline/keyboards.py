import asyncio

from FAQ.management.commands._loader import db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



class Keyboards:
    """Класс для управления клавиатурами бота"""

    def __init__(self):
        # Получение вопросов и связей из базы данных
        self.questions = list(db.get_all_questions())
        self.relations = list(db.get_relation_question())
        # Получение даты последнего изменения базы для контроля обновлений
        self.last_update = db.get_date()
        # Создание словарей клавиатур и ответов
        self.dict_keyboards = {str(x[2]): InlineKeyboardMarkup(row_wigth=2) for x in self.questions}
        self.dict_answers = {str(x[2]): str(x[1]) for x in self.questions}
        # Создание титульной клавиатуры, после нажатия кнопки /start
        self._title_keyboard()
        # Инициализация кнопок
        self.add_button_to_all("Вернуться на главную", "to_main")
        self.title_text = "Добрый день!\nКакой у вас вопрос?"
        self._all_keyboards()


    def _title_keyboard(self):
        """Создание стартовой клавиатуры"""
        self.title = InlineKeyboardMarkup(row_wigth=1)
        for i in self.questions:
            if i[3] == True:
                button = InlineKeyboardButton(text=i[0], callback_data=f"applic,{i[2]}")
                self.title.insert(button)

    def add_button_to_all(self, text, callback_data):
        """Функция для добавления кнопки во все клавиатуры кроме стартовой"""
        for key in self.dict_keyboards:
            try:
                if int(key):
                    self.relations.append((text, text, callback_data, key))
            except TypeError:
                print(key + " - не число")
        self.dict_keyboards.update({callback_data: text})


    def _all_keyboards(self):
        """Создание кнопок для дополнительных клавиатур"""
        for i in self.relations:
            for d in self.dict_keyboards.keys():
                if str(i[3]) == d:
                    button = InlineKeyboardButton(text=i[0], callback_data=f"applic,{i[2]}")
                    self.dict_keyboards[d].insert(button)


    async def bot_updater(self):
        """Обновление кнопок бота при обновлении базы данных"""
        while True:
            db.__init__()
            if self.last_update == db.get_date():
                pass
            else:
                self.__init__()
                print(f'Base updated {self.last_update[0][0].strftime("%d %B %Y %I:%M%p")}')
            await asyncio.sleep(5)

    def prnt(self):
        """Печать в консоль инициализированных для бота данных"""
        print(self.dict_keyboards)
        print(self.dict_answers)
        print(self.relations)

if __name__=='__main__':
    test = Keyboards()
    test.prnt()