import sqlite3

class dbconnector:
    # Подключение к базе данных
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    # Получаем вопросы для титульной страницы
    def get_general(self,general=True):
        with self.connection:
                 return self.cursor.execute("SELECT question, answer, id, general "
                                            "FROM FAQ_questions WHERE general = ?", (general,)).fetchall()

    # Получаем все вопросы из базы, чтобы не нагружать базу запросами
    def get_all_questions(self):
        with self.connection:
                 return self.cursor.execute("SELECT question, answer, id, general "
                                            "FROM FAQ_questions").fetchall()

    # Получаем связи вопросов
    def get_relation_question(self):
        with self.connection:
                 return self.cursor.execute("""SELECT question, answer, sub_id, base_id
                                                        FROM FAQ_relation_question as rq LEFT JOIN FAQ_questions as qu
                                                        ON qu.id = rq.sub_id""",).fetchall()
