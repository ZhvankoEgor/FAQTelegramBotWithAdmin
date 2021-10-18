import os
from subprocess import Popen

import psutil
from aiogram import executor
from django.core.management import BaseCommand
import sys

from FAQ.management.commands.handlers import dp


class Command(BaseCommand):
    help = 'Включение бота'

    def handle(self, *args, **options):
        if options['restart']:
            process_command = ['python3', 'manage.py', 'app']
            for process in psutil.process_iter():
                if process.cmdline() == process_command:
                    print('Process found. Terminating it.')
                    process.terminate()
                    break
            print('Process not found: starting it.')
            Popen(process_command)
        else:
            executor.start_polling(dp)

    def add_arguments(self, parser):
        parser.add_argument('-restart', action='store_const', const='restart')

    # def restart(self):
    #     process_command = ['python3', 'manage.py', 'app']
    #     for process in psutil.process_iter():
    #         if process.cmdline() == process_command:
    #             print('Process found. Terminating it.')
    #             process.terminate()
    #             break
    #     print('Process not found: starting it.')
    #     Popen(process_command)
