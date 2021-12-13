import asyncio
from subprocess import Popen
import psutil
from aiogram import executor
from django.core.management import BaseCommand
from FAQ.management.commands.handlers import dp
from FAQ.management.commands.handlers.users.questions import kb


async def on_startup(x):
    """Запуск асинхронных функций"""
    asyncio.create_task(kb.bot_updater())

class Command(BaseCommand):
    help = 'Включение бота'

    def handle(self, *args, **options):
        if options['restart']:
            direct_command = ['cd', '/media/sf_Projects/AdminForFAQ']
            process_command = ['python3', 'manage.py', 'app']
            for process in psutil.process_iter():
                if process.cmdline() == process_command:
                    print('Process found. Terminating it.')
                    process.terminate()
                    break
            print('Process not found: starting it.')
            Popen(direct_command)
            Popen(process_command)
        else:
            executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)

    def add_arguments(self, parser):
        parser.add_argument('-restart', action='store_const', const='restart')

