from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from FAQ.management.commands.keyboards.inline.keyboards import Keyboards
from FAQ.management.commands._loader import dp

# Создание экземпляра клавиатур
kb = Keyboards()


# Обработчик кнопки "Вернуться на главную", должен быть выше хендлера для обработки дополнительных вопросов
@dp.callback_query_handler(text_contains="to_main")
async def on_main(call: CallbackQuery):
    await call.answer(cache_time=20)
    await call.message.answer(text=kb.setting.title_text,
                              reply_markup=kb.title)
    await call.message.edit_reply_markup()


# Обработчик дополнительных вопросов
@dp.callback_query_handler(text_contains="applic")
async def applicate_mes(call: CallbackQuery):
    index = call.data.split(",")
    answer = kb.dict_answers[index[1]]
    await call.answer(cache_time=20)
    await call.message.answer(answer,
                              reply_markup=kb.dict_keyboards[index[1]])
    await call.message.edit_reply_markup()


# Стартовая страница
@dp.message_handler(Command("start"))
async def show_items(message: Message):
    await message.answer(text=kb.setting.title_text,
                         reply_markup=kb.title)
