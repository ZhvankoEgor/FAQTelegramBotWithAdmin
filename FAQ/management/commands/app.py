from aiogram import executor
from django.core.management import BaseCommand

from FAQ.management.commands.handlers import dp


class Command(BaseCommand):
    help = 'Включение бота'

    def handle(self, *args, **options):
        executor.start_polling(dp)
