from contextlib import suppress

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from FAQ.management.commands.keyboards.inline.callback_datas import title_text
from FAQ.management.commands.keyboards.inline.choice_buttons import title, dict_keyboards, dict_answers
from FAQ.management.commands._loader import dp


# Обработчик кнопки "Вернуться на главную", должен быть выше хендлера для обработки дополнительных вопросов
@dp.callback_query_handler(text_contains="to_main")
async def on_main(call: CallbackQuery):
    with suppress(MessageNotModified):
        await call.answer(cache_time=20)
        await call.message.answer(text=title_text,
                                  reply_markup=title)
        await call.message.edit_reply_markup()


# Обработчик дополнительных вопросов
@dp.callback_query_handler(text_contains="applic")
async def applicate_mes(call: CallbackQuery):
    with suppress(MessageNotModified):
        index = call.data.split(",")
        answer = dict_answers[index[1]]
        await call.answer(cache_time=20)
        await call.message.answer(answer,
                                  reply_markup=dict_keyboards[index[1]])
        await call.message.edit_reply_markup()

# Стартовая страница
@dp.message_handler(Command("start"))
async def show_items(message: Message):
    await message.answer(text=title_text,
                         reply_markup=title)

