import pymysql
from AdminForFAQ.settings import DATABASES


class DBConnector:
    """SQL запросы к базе данных"""

    def __init__(self):
        """Подключаемся к базе данных"""
        self.connection = pymysql.connect(host=DATABASES['default']['HOST'],
                                          user=DATABASES['default']['USER'],
                                          password=DATABASES['default']['PASSWORD'],
                                          db=DATABASES['default']['NAME'],
                                          charset='utf8mb4',
                                          )

    def get_bot_tokens(self):
        """Настройки бота"""
        query = """ SELECT  token
                    FROM FAQ_settingsbot
                    """
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


class BotQueries(DBConnector):
    """Запросы экземпляров бота"""

    def __init__(self, token):
        super().__init__()
        self.bot_id = self.get_bot_id(token)[0][0]

    def get_bot_id(self, token):
        """Получаем ID бота на основании токена"""
        query = """select id
                    FROM FAQ_settingsbot
                    WHERE token=%s"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, (token,))
            return cursor.fetchall()

    def get_all_questions(self):
        """Запрос всех вопросов из базы"""
        query = """ SELECT question, answer, id, general 
                    FROM FAQ_questions
                    WHERE bot_id=%s"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, (self.bot_id,))
            return cursor.fetchall()

    def get_relation_question(self):
        """Запрос связей вопросов"""
        query = """ SELECT question, answer, sub_id, base_id
                    FROM FAQ_relationquestion as rq 
                    LEFT JOIN FAQ_questions as qu
                    ON qu.id = rq.sub_id
                    WHERE bot_id=%s"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, (self.bot_id,))
            return cursor.fetchall()

    def get_date(self):
        """Дата последнего изменения в базе"""
        query = """ SELECT upd.bot_id, max(upd.updated) as last_update
                    FROM 
                        (   SELECT q.bot_id AS bot_id, max(rq.updated) AS updated
                            FROM FAQ_relationquestion as rq  left join FAQ_questions as q
                            ON rq.base_id = q.id
                            GROUP BY q.bot_id
                            union
                            SELECT id , max(updated)
                            FROM FAQ_settingsbot
                            GROUP BY id
                            union
                            SELECT bot_id, max(updated)
                            FROM FAQ_questions
                            GROUP BY bot_id) as upd
                    WHERE bot_id=%s
                    """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (self.bot_id,))
            return cursor.fetchall()

    def settings_bot(self):
        """Настройки бота"""
        query = """ SELECT  title_question, 
                            interval_refresh_base, 
                            title_button_row, 
                            other_button_row
                    FROM FAQ_settingsbot
                    WHERE id=%s"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, (self.bot_id,))
            return cursor.fetchall()

    def change_bot_status(self, token, status):
        """Указать статус бота"""
        query = """ UPDATE FAQ_settingsbot
                    SET status =%s
                    WHERE token =%s """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (status, token))
            self.connection.commit()


    def prnt(self):
        print(self.bot_id)


if __name__ == '__main__':
    BOT_TOKEN = "5011386007:AAGEz6LCB6HOOPzAZPA6ea-2s2dCVFEs7Ws"
    db = BotQueries(BOT_TOKEN)
    print(db.settings_bot())
    print(db.bot_id)
    print(db.get_date())
    db.change_bot_status(status="выключен",token="2006627411:AAHhOB2uPnxkEZIYrb8ECQ8py55axFl0rfA")
    print(db.get_all_questions())
    print(db.get_relation_question())
    last_update = db.get_date()
