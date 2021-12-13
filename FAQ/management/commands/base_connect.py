import pymysql
from AdminForFAQ.settings import DATABASES


class DB_connector:
    def __init__(self):
        """Подключаемся к базе данных"""
        self.connection = pymysql.connect(host=DATABASES['default']['HOST'],
                                          user=DATABASES['default']['USER'],
                                          password=DATABASES['default']['PASSWORD'],
                                          db=DATABASES['default']['NAME'],
                                          charset='utf8mb4',
                                          )

    def get_all_questions(self):
        """Запрос всех вопросов из базы"""
        query = """ SELECT question, answer, id, general 
                    FROM FAQ_questions"""
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_relation_question(self):
        """Запрос связей вопросов"""
        query = """ SELECT question, answer, sub_id, base_id
                    FROM FAQ_relation_question as rq 
                    LEFT JOIN FAQ_questions as qu
                    ON qu.id = rq.sub_id"""
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_date(self):
        """Дата последнего изменения в базе"""
        query = """ SELECT MAX(last_date)
                    FROM 
                        (   SELECT MAX(updated) as last_date
                            FROM FAQ_questions
                            union
                            SELECT MAX(updated)
                            FROM FAQ_relation_question) as ld
                    """
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


if __name__ == '__main__':
    db = DB_connector()
    # print(db.get_all_questions())
    # print(db.get_relation_question())
