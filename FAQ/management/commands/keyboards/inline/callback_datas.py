from FAQ.management.commands._config import db


title_text = "Добрый день!\n Какой у вас вопрос?"

# Загружаем данные из базы
questions = db.get_all_questions()  # Вопросы, которые мы будем рассылать
relations = db.get_relation_question()  # Информация о связях базовых и основных вопросов


