from time import sleep
import psutil
from subprocess import Popen
from django.core.management import BaseCommand
from .base_connect import DBConnector

db = DBConnector()


def set_from_tuple(db_tuple):
    """Преобразование кортежа из запроса во множество"""
    return {x[0] for x in db_tuple}


class Command(BaseCommand):
    """Класс для запуска скрипта через manage.py"""
    help = 'Запуск менеджера ботов'

    def handle(self, *args, **options):
        bm = BotsManager()
        bm.kill_process(set_from_tuple(bm.tokens))
        bm.run_process(set_from_tuple(bm.tokens))
        bm.update_checker()


class BotsManager:
    """Класс для управления запуском и остановкой ботов"""

    def __init__(self):
        self.tokens = db.get_bot_tokens()

    def update_checker(self):
        """Цикл проверяющий обновление токенов"""
        while True:
            db.__init__()
            if self.tokens == db.get_bot_tokens():
                print('Обновления токенов отсутствуют')
            else:
                self.update(self.tokens, db.get_bot_tokens())
                print('tokens updated')
            sleep(5)

    def update(self, old_tokens, new_tokens):
        """Завершает процесс удаленного из БД токена, и запускает процесс для добавленного"""
        old_tokens_set = set_from_tuple(old_tokens)
        new_tokens_set = set_from_tuple(new_tokens)
        killer_set = old_tokens_set - new_tokens_set
        run_set = new_tokens_set - old_tokens_set
        self.kill_process(killer_set)
        self.kill_process(run_set)
        self.run_process(run_set)
        self.__init__()

    def kill_process(self, *args):
        """Остановка процессов по токену бота"""
        for i in args[0]:
            process_command = ['python3', 'manage.py', 'app', i]
            for process in psutil.process_iter():
                if process.cmdline() == process_command:
                    print('Process found. Terminating it.')
                    process.terminate()
                    break

    def run_process(self, *args):
        """Запуск процессов по токену бота"""
        for i in args[0]:
            process_command = ['python3', 'manage.py', 'app', i]
            Popen(process_command)
